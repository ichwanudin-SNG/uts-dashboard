# Tugas 3 Kelompok — Pengujian Pricing

## 1. Struktur Proyek

```text
sdf05-tugas-pertemuan-10/
├── src/
│   └── pricing.py
├── tests/
│   └── test_pricing.py
├── .gitignore
├── .python-version
├── pyproject.toml
├── uv.lock
└── README.mdREADME.md
```

## 2. Cara Menjalankan Projek

### 1. Persyaratan

Pastikan Python 3.12 atau lebih baru dan `uv` sudah terpasang.

### 2. Masuk ke Direktori Projek

```bash
cd tugas3_kelompok
```

### 3. Instal Dependensi

Sinkronkan dependensi proyek menggunakan `uv`:

```bash
uv sync
```

### 4. Jalankan Unit Test

Jalankan seluruh unit test menggunakan perintah:

```bash
uv run pytest -v
```

Perintah tersebut menjalankan seluruh test dan menampilkan hasil setiap test secara terperinci.

## 3. Pengujian Mutasi

Pengujian mutasi dilakukan dengan mengubah implementasi `src/pricing.py` secara sengaja untuk memastikan unit test dapat mendeteksi kerusakan pada aturan bisnis. Setiap mutasi diuji secara terpisah, kemudian kode dikembalikan ke implementasi yang benar sebelum mutasi berikutnya.

### Tabel Hasil Pengujian Mutasi

| Kerusakan buatan                                                                                                        | Test yang gagal                                                                                                                                                                                        | Kesimpulan daya deteksi                                                                                                                    |
| ----------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------ |
| Menghapus penerapan diskon member sehingga fungsi `apply_member_discount()` selalu mengembalikan subtotal tanpa diskon. | `test_apply_member_discount_applies_ten_percent`; `test_calculate_total_for_member`. **2 test gagal.**                                                                                                 | Unit test mampu mendeteksi hilangnya diskon, baik melalui pengujian fungsi diskon secara langsung maupun perhitungan total belanja member. |
| Mengubah tarif pajak dari 11% menjadi 12% dengan mengubah `TAX_RATE = 0.11` menjadi `TAX_RATE = 0.12`.                  | `test_add_tax_applies_eleven_percent`; `test_calculate_total_for_member`; `test_calculate_total_for_non_member`; `test_calculate_total_defaults_to_non_member`. **4 test gagal.**                      | Unit test mampu mendeteksi perubahan tarif pajak pada fungsi pajak dan perhitungan total belanja untuk member maupun non-member.           |
| Menghapus validasi kuantitas `quantity <= 0` pada fungsi `calculate_subtotal()`.                                        | `test_calculate_subtotal_zero_quantity_raises_value_error`; `test_calculate_subtotal_negative_quantity_raises_value_error`; `test_calculate_total_zero_quantity_raises_value_error`. **3 test gagal.** | Unit test mampu mendeteksi hilangnya validasi kuantitas nol dan negatif, baik pada perhitungan subtotal maupun total belanja.              |

### Ringkasan hasil mutasi

| Mutasi                       | Test gagal | Test lulus | Status     |
| ---------------------------- | ---------: | ---------: | ---------- |
| Menghapus diskon             |          2 |         17 | Terdeteksi |
| Mengubah tarif pajak         |          4 |         15 | Terdeteksi |
| Menghapus validasi kuantitas |          3 |         16 | Terdeteksi |

## 4. Bukti Pengujian pada Implementasi yang Benar

Setelah semua mutasi selesai, implementasi `pricing.py` dikembalikan ke kode yang benar. Pengujian kemudian dijalankan menggunakan perintah:

```bash
python -m pytest -v
```

Ringkasan keluaran aktual:

```text
tests/test_pricing.py::test_calculate_subtotal_valid_inputs[10000-2-20000] PASSED             [  5%]
tests/test_pricing.py::test_calculate_subtotal_valid_inputs[15000-3-45000] PASSED             [ 10%]
tests/test_pricing.py::test_calculate_subtotal_valid_inputs[0-5-0] PASSED                     [ 15%]
tests/test_pricing.py::test_calculate_subtotal_negative_price_raises_value_error PASSED       [ 21%]
tests/test_pricing.py::test_calculate_subtotal_zero_quantity_raises_value_error PASSED        [ 26%]
tests/test_pricing.py::test_calculate_subtotal_negative_quantity_raises_value_error PASSED    [ 31%]
tests/test_pricing.py::test_apply_member_discount_applies_ten_percent PASSED                  [ 36%]
tests/test_pricing.py::test_apply_member_discount_non_member_pays_full_price PASSED           [ 42%]
tests/test_pricing.py::test_apply_member_discount_zero_subtotal PASSED                        [ 47%]
tests/test_pricing.py::test_add_tax_applies_eleven_percent PASSED                             [ 52%]
tests/test_pricing.py::test_add_tax_zero_amount PASSED                                        [ 57%]
tests/test_pricing.py::test_calculate_total_for_member PASSED                                 [ 63%]
tests/test_pricing.py::test_calculate_total_for_non_member PASSED                             [ 68%]
tests/test_pricing.py::test_calculate_total_defaults_to_non_member PASSED                     [ 73%]
tests/test_pricing.py::test_calculate_total_negative_price_raises_value_error PASSED          [ 78%]
tests/test_pricing.py::test_calculate_total_zero_quantity_raises_value_error PASSED           [ 84%]
tests/test_pricing.py::test_write_receipt_writes_lines_with_final_newline PASSED              [ 89%]
tests/test_pricing.py::test_write_receipt_with_empty_lines PASSED                             [ 94%]
tests/test_pricing.py::test_write_receipt_overwrites_existing_file PASSED                     [100%]

======================================== 19 passed in 0.05s =========================================
```

# 5. Pertanyaan Analisis

### 1. Jelaskan mengapa perbandingan hasil perhitungan bilangan floating point sebaiknya memakai `pytest.approx` alih-alih perbandingan kesetaraan langsung.

Bilangan floating point tidak selalu dapat direpresentasikan secara tepat dalam komputer. `pytest.approx` memungkinkan perbandingan dengan toleransi kecil sehingga perbedaan pembulatan tidak menyebabkan test gagal.

### 2. Jelaskan mengapa test yang memanggil berkas nyata di dalam direktori proyek lebih berisiko dibandingkan penggunaan `tmp_path`.

`tmp_path` menyediakan direktori sementara yang terisolasi untuk setiap test. Ini mencegah test menimpa berkas proyek dan mengurangi efek samping antar-test.

### 3. Jelaskan satu test pada hasil pekerjaan Anda yang menurut Anda paling lemah, beserta alasan dan usulan perbaikannya.

`test_add_tax_zero_amount()` relatif lemah karena implementasi yang tidak menambahkan pajak tetap bisa lulus untuk input nol.

Perbaikan: uji nilai positif, misalnya `assert add_tax(100000) == pytest.approx(111000)`.

### 4. Jelaskan bagaimana hasil pengujian mutasi mengubah cara Anda menilai kualitas sebuah test.

Test yang lulus belum tentu mampu mendeteksi kesalahan. Pengujian mutasi mengukur kemampuan test menemukan kerusakan yang disengaja. Mutasi yang menyebabkan test gagal menunjukkan bahwa assertion terkait mampu mendeteksi kesalahan tersebut.

### 5. Jelaskan padanan antara pytest.raises , pytest.mark.parametrize , dan fixture pada PyTest dengan fitur yang setara pada JUnit 5.

| Fitur PyTest              | Padanan JUnit 5                                                                       | Fungsi                                                           |
| ------------------------- | ------------------------------------------------------------------------------------- | ---------------------------------------------------------------- |
| `pytest.raises`           | `assertThrows()`                                                                      | Memastikan suatu operasi menghasilkan exception yang diharapkan. |
| `pytest.mark.parametrize` | `@ParameterizedTest` dengan `@CsvSource`, `@ValueSource`, atau sumber argumen lainnya | Menjalankan test yang sama dengan beberapa kombinasi input.      |
| Fixture PyTest            | `@BeforeEach`, `@AfterEach`, atau metode beranotasi lain sesuai siklus hidup test     | Menyiapkan dan membersihkan kebutuhan pengujian.                 |

### 6. Jelaskan mengapa pernyataan "total anggota selalu lebih besar daripada subtotal" merupakan asumsi yang keliru pada modul ini, dengan menunjukkan perhitungannya.

Member mendapat diskon 10%, kemudian dikenai pajak 11%.

Contoh subtotal Rp100.000:

- Setelah diskon: Rp100.000 × 0,90 = Rp90.000
- Setelah pajak: Rp90.000 × 1,11 = Rp99.900

Rumusnya:

$$
\text{Total}=\text{Subtotal}\times0{,}90\times1{,}11
$$

Karena faktor pengalinya adalah `0,999`, total member justru sedikit lebih kecil daripada subtotal awal.
