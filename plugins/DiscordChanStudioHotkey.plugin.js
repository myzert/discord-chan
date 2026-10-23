/**
 * @name DiscordChanStudioHotkey
 * @author Discord-Chan Team
 * @version 1.0.0
 * @description Press Ctrl+Shift+P directly inside Discord to instantly open the Discord-Chan Studio / Command Palette!
 * @source https://github.com/myzert/discord-chan
 */

module.exports = class DiscordChanStudioHotkey {
    start() {
        this.handleKeydown = (e) => {
            if (e.ctrlKey && e.shiftKey && (e.code === "KeyP" || e.key === "P" || e.key === "p")) {
                e.preventDefault();
                e.stopPropagation();
                try {
                    const cp = require("child_process");
                    cp.exec("/usr/local/bin/discord-chan-custom </dev/null >/dev/null 2>&1 &");
                } catch (err) {
                    console.error("[DiscordChanStudioHotkey] Failed to spawn studio:", err);
                }
            }
        };
        window.addEventListener("keydown", this.handleKeydown, true);
        console.log("[DiscordChanStudioHotkey] Ready! Press Ctrl+Shift+P to open Discord-Chan Studio.");
    }
    stop() {
        if (this.handleKeydown) {
            window.removeEventListener("keydown", this.handleKeydown, true);
        }
    }
};
