from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Barang(BaseModel):
    id: Optional[int] = None
    nama: str
    penanggung_jawab: str
    kategori: str
    stok: int

barang_list: List[Barang] = [
    Barang(id=1, nama="Meja Kerja Kayu", penanggung_jawab="Staff TU", kategori="Perabot", stok=12),
    Barang(id=2, nama="Kursi Kantor Putar", penanggung_jawab="Staff TU", kategori="Perabot", stok=8),
    Barang(id=3, nama="Lemari Arsip 4 Pintu", penanggung_jawab="Arsiparis", kategori="Penyimpanan", stok=3),
    Barang(id=4, nama="Komputer Desktop i5", penanggung_jawab="Bagian IT", kategori="Elektronik", stok=15),
    Barang(id=5, nama="Layar Proyektor Gantung", penanggung_jawab="Bagian Sarana", kategori="Elektronik", stok=4),
    Barang(id=6, nama="Proyektor LCD 3000ANSI", penanggung_jawab="Bagian Sarana", kategori="Elektronik", stok=2),
    Barang(id=7, nama="Papan Tulis Putih Besar", penanggung_jawab="Bagian Sarana", kategori="Perabot", stok=6),
    Barang(id=8, nama="Kursi Hadap Plastik", penanggung_jawab="Petugas Kebersihan", kategori="Perabot", stok=25),
    Barang(id=9, nama="Rak Buku 6 Tingkat", penanggung_jawab="Perpustakaan", kategori="Penyimpanan", stok=5),
    Barang(id=10, nama="Mesin Fotokopi Digital", penanggung_jawab="Tata Usaha", kategori="Elektronik", stok=1),
    Barang(id=11, nama="Kipas Angin Gantung", penanggung_jawab="Petugas Kebersihan", kategori="Elektronik", stok=18),
    Barang(id=12, nama="Pintu Kaca Geser Ruang Rapat", penanggung_jawab="Pemeliharaan", kategori="Bangunan", stok=2),
    Barang(id=13, nama="Jam Dinding Otomatis", penanggung_jawab="Petugas Kebersihan", kategori="Lainnya", stok=7),
    Barang(id=14, nama="Telepon Kantor Kabel", penanggung_jawab="Tata Usaha", kategori="Elektronik", stok=4),
    Barang(id=15, nama="Kotak P3K Lengkap", penanggung_jawab="Petugas Kesehatan", kategori="Keselamatan", stok=6),
    Barang(id=16, nama="Alat Pemadam Api Ringan", penanggung_jawab="Satpam", kategori="Keselamatan", stok=10),
    Barang(id=17, nama="Timbangan Digital Barang", penanggung_jawab="Gudang", kategori="Alat Ukur", stok=2),
    Barang(id=18, nama="Tangga Lipat 4 Tingkat", penanggung_jawab="Pemeliharaan", kategori="Alat Bantu", stok=3),
    Barang(id=19, nama="Kabel LAN 100 Meter", penanggung_jawab="Bagian IT", kategori="Perlengkapan", stok=5),
    Barang(id=20, nama="Papan Nama Ruangan Akrilik", penanggung_jawab="Tata Usaha", kategori="Perlengkapan", stok=9),
]

@app.get("/barang")
def ambil_semua_barang():
    return barang_list

@app.post("/barang")
def tambah_barang(barang: Barang):
    barang.id = max([b.id for b in barang_list], default=0) + 1
    barang_list.append(barang)
    return barang

@app.delete("/barang/{barang_id}")
def hapus_barang(barang_id: int):
    global barang_list
    barang_list = [b for b in barang_list if b.id != barang_id]
    return {"pesan": "Barang berhasil dihapus"}