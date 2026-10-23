# 🧩 Chrome-Style Extension System (.zip)

Discord-Chan includes a modular extension architecture that allows anyone to create, package, and distribute custom add-ons as standard `.zip` files.

### 📦 Extension ZIP Structure:
```
my-extension.zip/
├── manifest.json   (Required: extension metadata)
├── style.css       (Custom CSS rules)
├── plugin.js       (Optional: BetterDiscord JavaScript plugin)
└── README.txt      (Optional documentation)
```

### 📄 Sample `manifest.json`:
```json
{
  "id": "my-cool-glow",
  "name": "Custom Neon Glow",
  "version": "1.0.0",
  "author": "myzert",
  "description": "Adds glowing borders and custom fonts to Discord",
  "styles": "style.css",
  "script": "plugin.js"
}
```

### 🚀 Creating an Extension with Studio:
1. Open Discord-Chan Studio (`Ctrl+Shift+P`).
2. Navigate to `#  plugin-extensions-zip`.
3. Click **[Create Extension Template (.zip)]**.
4. Extract the generated template, edit `style.css`, re-zip, and click **[Install Extension (.zip)]**!
