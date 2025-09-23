import discord
from discord import app_commands
from discord.ext import commands


ERRORS = [
    ("socket", "device socket io failed", -1),
    ("pem_parse_failed", "PEM parse failed", -2),
    ("rustls", "TLS error", -3),
    ("tls_builder_failed", "TLS verifiction build failed", -4),
    ("plist", "io on plist", -5),
    ("utf8", "can't convert bytes to utf8", -6),
    ("unexpected_response", "unexpected response from device", -7),
    ("get_prohibited", "this request was prohibited", -8),
    ("session_inactive", "no SSL session is active", -9),
    ("invalid_host_id", "device does not have pairing file", -10),
    ("no_established_connection", "no established connection", -11),
    ("heartbeat_sleepy_time", "device went to sleep", -12),
    ("heartbeat_timeout", "heartbeat timeout", -13),
    ("not_found", "not found", -14),
    ("service_not_found", "service not found", -15),
    ("cdtunnel_packet_too_short", "CDTunnel packet too short", -16),
    ("cdtunnel_packet_invalid_magic", "CDTunnel packet invalid magic", -17),
    ("packet_size_mismatch", "Proclaimed packet size does not match actual size", -18),
    ("json", "JSON serialization failed", -19),
    ("device_not_found", "device not found", -20),
    ("device_locked", "device lockded", -21),
    ("usb_connection_refused", "device refused connection", -22),
    ("usb_bad_command", "bad command", -23),
    ("usb_bad_device", "bad device", -24),
    ("usb_bad_version", "usb bad version", -25),
    ("bad_build_manifest", "bad build manifest", -26),
    ("image_not_mounted", "image not mounted", -27),
    ("pairing_dialog_response_pending", "pairing trust dialog pending", -28),
    ("user_denied_pairing", "user denied pairing trust", -29),
    ("password_protected", "device is locked", -30),
    ("misagent_failure", "misagent operation failed", -31),
    ("installation_proxy_operation_failed", "installation proxy operation failed", -32),
    ("afc", "afc error", -33),
    ("unknown_afc_opcode", "unknown afc opcode", -34),
    ("invalid_afc_magic", "invalid afc magic", -35),
    ("afc_missing_attribute", "missing file attribute", -36),
    ("crash_report_mover_bad_response", "crash report mover sent the wrong response", -37),
    ("reqwest", "http reqwest error", -38),
    ("internal_error", "internal error", -39),
    ("unknown_frame", "unknown http frame type", -40),
    ("unknown_http_setting", "unknown http setting type", -41),
    ("uninitialized_stream_id", "Unintialized stream ID", -42),
    ("unknown_xpc_type", "unknown XPC type", -43),
    ("malformed_xpc", "malformed XPC message", -44),
    ("invalid_xpc_magic", "invalid XPC magic", -45),
    ("unexpected_xpc_version", "unexpected XPC version", -46),
    ("invalid_c_string", "invalid C string", -47),
    ("http_stream_reset", "stream reset", -48),
    ("http_go_away", "go away packet received", -49),
    ("ns_keyed_archive_error", "NSKeyedArchive error", -50),
    ("unknown_aux_value_type", "Unknown aux value type", -51),
    ("unknown_channel", "unknown channel", -52),
    ("addr_parse_error", "cannot parse string as IpAddr", -53),
    ("disable_memory_limit_failed", "disable memory limit failed", -54),
    ("not_enough_bytes", "not enough bytes", -55),
    ("utf8_error", "failed to parse bytes as valid utf8", -56),
    ("invalid_argument", "invalid argument passed", -57),
    ("unknown_error_type", "unknown error returned from device", -59),
    ("ffi_invalid_arg", "invalid arguments were passed", -60),
    ("ffi_invalid_string", "invalid string was passed", -61),
    ("ffi_buffer_too_small", "buffer passed is too small", -62),
    ("unsupported_watch_key", "unsupported watch key", -63),
    ("malformed_command", "malformed command", -64),
    ("integer_overflow", "integer overflow", -65),
    ("canceled_by_user", "canceled by user", -66),
    ("malformed_package_archive", "malformed package archive", -67),
]


class ErrorCodes(commands.Cog, name="errorcodes"):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.key_to_data = {k: (t, c) for k, t, c in ERRORS}
        self.code_to_key = {c: k for k, _, c in ERRORS}

    async def errorcode_autocomplete(self, interaction: discord.Interaction, current: str):
        current_lower = current.lower()
        items = []
        for key, (title, code) in self.key_to_data.items():
            if not current or current_lower in key.lower() or current_lower in title.lower() or current_lower in str(code):
                items.append(app_commands.Choice(name=f"{key} • {title} ({code})", value=key))
                if len(items) >= 25:
                    break
        return items

    @app_commands.command(name="errorcode", description="Look up an idevice error code by name or number")
    @app_commands.describe(name="Start typing to search all error names and codes")
    @app_commands.autocomplete(name=errorcode_autocomplete)
    async def errorcode(self, interaction: discord.Interaction, name: str):
        key = name
        if key not in self.key_to_data:
            try:
                num = int(name)
                key = self.code_to_key.get(num)
            except ValueError:
                key = None
        if key is None or key not in self.key_to_data:
            await interaction.response.send_message("Error not found.", ephemeral=True)
            return
        title, code = self.key_to_data[key]
        embed = discord.Embed(
            title=title,
            description=f"Code: `{code}`\nName: `{key}`",
            color=0xfa8c4a,
        )
        embed.set_author(name="idevice", icon_url="https://yes.nighty.works/raw/snLMuO.png")
        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot) -> None:
    cog = ErrorCodes(bot)
    await bot.add_cog(cog)


