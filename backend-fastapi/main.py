from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# Izinkan akses dari frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Buku(BaseModel):
    id: Optional[int] = None
    judul: str
    penulis: str
    kategori: str
    stok: int

# Data awal
buku_list: List[Buku] = [
    Buku(id=1, judul="Belajar Python", penulis="Budi", kategori="Pemrograman", stok=5),
    Buku(id=2, judul="Vue.js 3 Lengkap", penulis="Ani", kategori="Pemrograman", stok=2),
    Buku(id=3, judul="Dasar Basis Data", penulis="Siti", kategori="Teknik", stok=4),
    Buku(id=4, judul="Desain Web Modern", penulis="Dedi", kategori="Desain", stok=3),
    Buku(id=5, judul="Algoritma Pemrograman", penulis="Eka", kategori="Pemrograman", stok=6),
    Buku(id=6, judul="Jaringan Komputer", penulis="Farhan", kategori="Teknik", stok=2),
    Buku(id=7, judul="Manajemen Proyek IT", penulis="Gita", kategori="Manajemen", stok=4),
    Buku(id=8, judul="Keamanan Sistem", penulis="Hendra", kategori="Teknik", stok=3),
    Buku(id=9, judul="Statistika Data", penulis="Ika", kategori="Dasar", stok=5),
    Buku(id=10, judul="Kecerdasan Buatan", penulis="Joko", kategori="Pemrograman", stok=1),
]

@app.get("/buku")
def ambil_semua_buku():
    return buku_list

@app.post("/buku")
def tambah_buku(buku: Buku):
    buku.id = max([b.id for b in buku_list], default=0) + 1
    buku_list.append(buku)
    return buku

@app.delete("/buku/{buku_id}")
def hapus_buku(buku_id: int):
    global buku_list
    buku_list = [b for b in buku_list if b.id != buku_id]
    return {"pesan": "Berhasil dihapus"}