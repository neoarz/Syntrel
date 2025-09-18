import aiosqlite
import asyncio
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class TagButton:
    id: int
    tag_id: int
    label: str
    url: str
    emoji: Optional[str] = None


@dataclass
class Tag:
    tid: int
    name: str
    content: str
    author: int
    guild: Optional[int]
    used: int = 0
    buttons: List[TagButton] = None

    def __post_init__(self):
        if self.buttons is None:
            self.buttons = []


class AsyncTagManager:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._connection = None
        self._tags_cache = None

    @classmethod
    async def from_file(cls, db_path: str):
        manager = cls(db_path)
        await manager._connect()
        return manager

    async def _connect(self):
        self._connection = await aiosqlite.connect(self.db_path)
        await self._load_tags()

    async def close(self):
        if self._connection:
            await self._connection.close()
            self._connection = None

    async def _load_tags(self):
        if not self._connection:
            return

        cursor = await self._connection.execute("""
            SELECT t.tid, t.name, t.content, t.author, t.guild, t.used,
                   b.id, b.label, b.url, b.emoji
            FROM tags t
            LEFT JOIN tag_buttons b ON t.tid = b.tag_id
            ORDER BY t.tid
        """)
        
        rows = await cursor.fetchall()
        await cursor.close()

        tags_dict = {}
        for row in rows:
            tid = row[0]
            if tid not in tags_dict:
                tags_dict[tid] = Tag(
                    tid=row[0],
                    name=row[1],
                    content=row[2],
                    author=row[3],
                    guild=row[4],
                    used=row[5],
                    buttons=[]
                )
            
            if row[6] is not None:
                button = TagButton(
                    id=row[6],
                    tag_id=tid,
                    label=row[7],
                    url=row[8],
                    emoji=row[9]
                )
                tags_dict[tid].buttons.append(button)

        self._tags_cache = list(tags_dict.values())

    @property
    async def tags(self) -> List[Tag]:
        if self._tags_cache is None:
            await self._load_tags()
        return self._tags_cache

    async def tag(self, tid: int = None, name: str = None) -> Optional[Tag]:
        tags = await self.tags
        if tid is not None:
            return next((tag for tag in tags if tag.tid == tid), None)
        if name is not None:
            return next((tag for tag in tags if tag.name.lower() == name.lower()), None)
        return None

    async def create_tag(self, name: str, content: str, author: int, guild: Optional[int] = None) -> Tag:
        if not self._connection:
            raise ValueError("Database not connected")

        cursor = await self._connection.execute(
            "INSERT INTO tags (name, content, author, guild) VALUES (?, ?, ?, ?)",
            (name, content, author, guild)
        )
        await self._connection.commit()
        
        tid = cursor.lastrowid
        await cursor.close()

        tag = Tag(tid=tid, name=name, content=content, author=author, guild=guild, used=0, buttons=[])
        self._tags_cache.append(tag)
        return tag

    async def update(self, tag: Tag):
        if not self._connection:
            raise ValueError("Database not connected")

        await self._connection.execute(
            "UPDATE tags SET name=?, content=?, used=? WHERE tid=?",
            (tag.name, tag.content, tag.used, tag.tid)
        )
        await self._connection.commit()

        if self._tags_cache:
            for i, cached_tag in enumerate(self._tags_cache):
                if cached_tag.tid == tag.tid:
                    self._tags_cache[i] = tag
                    break

    async def delete_tag(self, tag: Tag):
        if not self._connection:
            raise ValueError("Database not connected")

        await self._connection.execute("DELETE FROM tags WHERE tid=?", (tag.tid,))
        await self._connection.commit()

        if self._tags_cache:
            self._tags_cache = [t for t in self._tags_cache if t.tid != tag.tid]

    async def add_button(self, tag: Tag, label: str, url: str, emoji: Optional[str] = None) -> TagButton:
        if not self._connection:
            raise ValueError("Database not connected")

        cursor = await self._connection.execute(
            "INSERT INTO tag_buttons (tag_id, label, url, emoji) VALUES (?, ?, ?, ?)",
            (tag.tid, label, url, emoji)
        )
        await self._connection.commit()
        
        button_id = cursor.lastrowid
        await cursor.close()

        button = TagButton(id=button_id, tag_id=tag.tid, label=label, url=url, emoji=emoji)
        tag.buttons.append(button)
        return button

    async def update_button(self, button: TagButton):
        if not self._connection:
            raise ValueError("Database not connected")

        await self._connection.execute(
            "UPDATE tag_buttons SET label=?, url=?, emoji=? WHERE id=?",
            (button.label, button.url, button.emoji, button.id)
        )
        await self._connection.commit()

    async def delete_button(self, button: TagButton):
        if not self._connection:
            raise ValueError("Database not connected")

        await self._connection.execute("DELETE FROM tag_buttons WHERE id=?", (button.id,))
        await self._connection.commit()

        for tag in await self.tags:
            if tag.tid == button.tag_id:
                tag.buttons = [b for b in tag.buttons if b.id != button.id]
                break
