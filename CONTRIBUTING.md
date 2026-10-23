# 🤝 Panduan Kontribusi / Contributing to Discord-Chan

[English](#english) | [Bahasa Indonesia](#bahasa-indonesia)

---

<a name="english"></a>
## 🌸 English: Welcome Contributors!

We love and welcome contributions from the anime and customization community! Whether you want to add new anime wallpapers, design aesthetic color palettes, improve zero-lag CSS performance, or translate documentation, your help is appreciated.

### 🌟 How You Can Help
1. ⭐ **Star this repository:** Show your support by giving a star on GitHub!
2. 🖼️ **Submit New Anime Wallpapers:**
   - Must be high quality (minimum 1920x1080, preferably 2K/4K).
   - Place image files inside `assets/wallpapers/`.
   - Register it in `src/studio.py` under `WALLPAPERS`.
3. 🎨 **Add New Color Palettes:**
   - Propose beautiful color pairs (`accent_color`, `soft_pink`) in `src/studio.py`.
4. ⚡ **Zero-Lag & CSS Improvements:**
   - Maintain the zero-lag rule: no heavy `box-shadow` or rasterized `backdrop-filter: blur`.
5. 🌐 **Translations:**
   - Add or improve language files for community members worldwide.

### 🚀 Pull Request Workflow
1. Fork the repo: `https://github.com/myzert/discord-chan`
2. Create a branch: `git checkout -b feature/my-cool-anime-theme`
3. Commit your changes: `git commit -m "feat: Add new anime preset"`
4. Push to branch: `git push origin feature/my-cool-anime-theme`
5. Submit a Pull Request on GitHub!

All contributors will be featured automatically on the **Contributor Wall** in `README.md`!

---

<a name="bahasa-indonesia"></a>
## 🌸 Bahasa Indonesia: Selamat Datang Para Kontributor!

Kami sangat menyambut kontribusi dari teman-teman komunitas anime dan Discord! Kamu bisa berkontribusi dengan menambahkan wallpaper anime baru, mendesain palet warna baru, menyempurnakan performa CSS, atau menerjemahkan panduan.

### 🌟 Cara Berkontribusi
1. ⭐ **Beri Star pada repo ini:** Dukung proyek ini dengan menekan tombol Star di pojok kanan atas!
2. 🖼️ **Kirim Wallpaper Anime Baru:**
   - Resolusi minimal Full HD (1920x1080) atau 4K.
   - Masukkan gambar ke folder `assets/wallpapers/`.
   - Daftarkan nama wallpaper pada list `WALLPAPERS` di `src/studio.py`.
3. 🎨 **Buat Palet Warna Baru:**
   - Tambahkan kombinasi hex warna estetik pada list `PINK_PALETTES` di `src/studio.py`.
4. ⚡ **Optimasi Performa & CSS:**
   - Jaga prinsip zero-lag: jangan tambahkan efek shadow berat yang membebani GPU.

### 🚀 Alur Mengirim Pull Request (PR):
1. Fork repository: `https://github.com/myzert/discord-chan`
2. Buat branch baru: `git checkout -b fitur-wallpaper-anime`
3. Simpan perubahan: `git commit -m "feat: Tambah preset anime"`
4. Push ke GitHub: `git push origin fitur-wallpaper-anime`
5. Buka Pull Request di GitHub!
