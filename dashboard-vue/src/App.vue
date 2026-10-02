<template>
  <div style="padding: 20px; font-family: Arial;">
    <h1>📚 Dashboard Perpustakaan</h1>

    <div style="display: flex; gap: 20px; margin: 20px 0;">
      <div class="kartu">
        <h3>Total Buku</h3>
        <p>{{ bukuList.length }}</p>
      </div>
      <div class="kartu">
        <h3>Stok Menipis</h3>
        <p>{{ bukuList.filter(b => b.stok <= 3).length }}</p>
      </div>
      <div class="kartu">
        <h3>Total Eksemplar</h3>
        <p>{{ bukuList.reduce((s, b) => s + b.stok, 0) }}</p>
      </div>
    </div>

    <div style="margin: 20px 0;">
      <input v-model="cari" placeholder="Cari judul/penulis..." style="padding: 8px; width: 250px;">
      <select v-model="urutan" style="padding: 8px; margin-left: 8px;">
        <option value="az">Urut A-Z</option>
        <option value="za">Urut Z-A</option>
        <option value="stok">Stok Terbanyak</option>
      </select>
    </div>

    <div style="margin: 20px 0; display: flex; gap: 8px;">
      <input v-model="baru.judul" placeholder="Judul" style="padding: 8px; flex: 1;">
      <input v-model="baru.penulis" placeholder="Penulis" style="padding: 8px; flex: 1;">
      <input v-model="baru.kategori" placeholder="Kategori" style="padding: 8px; flex: 1;">
      <input v-model.number="baru.stok" type="number" placeholder="Stok" style="padding: 8px; width: 100px;">
      <button @click="tambahBuku" style="padding: 8px 16px; background: #4CAF50; color: white; border: none; border-radius: 4px;">+ Tambah</button>
    </div>

    <table border="1" cellpadding="10" cellspacing="0" style="width: 100%; margin-top: 20px;">
      <thead>
        <tr style="background: #f0f0f0;">
          <th>Judul</th>
          <th>Penulis</th>
          <th>Kategori</th>
          <th>Stok</th>
          <th>Aksi</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="buku in bukuTampil" :key="buku.id">
          <td>{{ buku.judul }}</td>
          <td>{{ buku.penulis }}</td>
          <td>{{ buku.kategori }}</td>
          <td :style="{ color: buku.stok <= 3 ? 'red' : 'green' }">{{ buku.stok }}</td>
          <td><button @click="hapusBuku(buku.id)" style="color: red; border: none; background: none; cursor: pointer;">Hapus</button></td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

// === PENTING: Pilih SATU alamat di bawah ini ===
// Kalau pakai 127.0.0.1 di browser, pakai yang ini:
const ALAMAT = 'http://127.0.0.1:8000/buku'
// Kalau pakai localhost di browser, pakai yang ini:
// const ALAMAT = 'http://localhost:8000/buku'

const bukuList = ref([])
const cari = ref('')
const urutan = ref('az')
const baru = ref({ judul: '', penulis: '', kategori: '', stok: 1 })

const ambilData = async () => {
  try {
    const res = await fetch(ALAMAT)
    bukuList.value = await res.json()
  } catch (e) {
    alert('Gagal ambil data! Pastikan backend menyala di ' + ALAMAT)
  }
}

const tambahBuku = async () => {
  if (!baru.value.judul) return
  await fetch(ALAMAT, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(baru.value)
  })
  baru.value = { judul: '', penulis: '', kategori: '', stok: 1 }
  ambilData()
}

const hapusBuku = async (id) => {
  await fetch(`${ALAMAT}/${id}`, { method: 'DELETE' })
  ambilData()
}

const bukuTampil = computed(() => {
  let hasil = bukuList.value.filter(b =>
    b.judul.toLowerCase().includes(cari.value.toLowerCase()) ||
    b.penulis.toLowerCase().includes(cari.value.toLowerCase())
  )
  if (urutan.value === 'az') hasil.sort((a, b) => a.judul.localeCompare(b.judul))
  if (urutan.value === 'za') hasil.sort((a, b) => b.judul.localeCompare(a.judul))
  if (urutan.value === 'stok') hasil.sort((a, b) => b.stok - a.stok)
  return hasil
})

onMounted(ambilData)
</script>