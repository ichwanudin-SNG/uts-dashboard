<template>
  <div class="wadah">
    <h1>📋 Daftar Barang Inventaris</h1>

    <!-- Ringkasan -->
    <div class="ringkasan">
      <div class="kotak">
        <h3>Total Barang</h3>
        <p>{{ totalBarang }}</p>
      </div>
      <div class="kotak">
        <h3>Stok Menipis + Habis</h3>
        <p>{{ stokMenipisDanHabis }}</p>
      </div>
      <div class="kotak">
        <h3>Jumlah Kategori</h3>
        <p>{{ jumlahKategori }}</p>
      </div>
      <div class="kotak">
        <h3>Total Unit</h3>
        <p>{{ totalUnit }}</p>
      </div>
    </div>

    <!-- Pencarian & Urutan -->
    <div class="kontrol">
      <input
        v-model="kataKunci"
        type="text"
        placeholder="Cari nama barang / penanggung jawab..."
      />
      <select v-model="urutan">
        <option value="">Urutkan...</option>
        <option value="az">Nama A-Z</option>
        <option value="za">Nama Z-A</option>
        <option value="stokBanyak">Stok Terbanyak</option>
        <option value="stokSedikit">Stok Tersedikit</option>
      </select>
    </div>

    <!-- Form Tambah -->
    <div class="form-tambah">
      <input v-model="baru.nama" type="text" placeholder="Nama Barang" />
      <input v-model="baru.penanggung_jawab" type="text" placeholder="Penanggung Jawab" />
      <input v-model="baru.kategori" type="text" placeholder="Kategori" />
      <input v-model.number="baru.stok" type="number" placeholder="Jumlah Stok" min="0" />
      <button @click="kirimBarang" class="btn-tambah">+ Tambah</button>
    </div>

    <!-- Tabel -->
    <table>
      <thead>
        <tr>
          <th>Nama Barang</th>
          <th>Penanggung Jawab</th>
          <th>Kategori</th>
          <th>Stok</th>
          <th>Status</th>
          <th>Aksi</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in daftarTampil" :key="item.id">
          <td>{{ item.nama }}</td>
          <td>{{ item.penanggung_jawab }}</td>
          <td>{{ item.kategori }}</td>
          <td class="stok" :class="kelasStatus(item.stok)">{{ item.stok }}</td>
          <td>
            <span class="badge" :class="kelasStatus(item.stok)">
              {{ ambilStatus(item.stok) }}
            </span>
          </td>
          <td>
            <button @click="hapusData(item.id)" class="btn-hapus">Hapus</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

// Alamat backend
const ALAMAT = 'http://localhost:8000/barang'

// Data
const daftarBarang = ref([])
const kataKunci = ref('')
const urutan = ref('')
const baru = ref({ nama: '', penanggung_jawab: '', kategori: '', stok: 0 })

// Ambil data dari backend
const ambilData = async () => {
  try {
    const res = await fetch(ALAMAT)
    daftarBarang.value = await res.json()
  } catch {
    alert('Gagal ambil data! Pastikan backend menyala di http://127.0.0.1:8000/barang')
    daftarBarang.value = []
  }
}

// Tentukan status & warna
const ambilStatus = (stok) => {
  if (stok === 0) return 'Habis'
  if (stok <= 3) return 'Menipis'
  return 'Aman'
}

const kelasStatus = (stok) => {
  if (stok === 0) return 'habis'
  if (stok <= 3) return 'menipis'
  return 'aman'
}

// Filter & urut
const daftarTampil = computed(() => {
  let hasil = [...daftarBarang.value]

  // Cari
  if (kataKunci.value) {
    const kunci = kataKunci.value.toLowerCase()
    hasil = hasil.filter(b =>
      b.nama.toLowerCase().includes(kunci) ||
      b.penanggung_jawab.toLowerCase().includes(kunci)
    )
  }

  // Urut
  if (urutan.value === 'az') {
    hasil.sort((a, b) => a.nama.localeCompare(b.nama))
  } else if (urutan.value === 'za') {
    hasil.sort((a, b) => b.nama.localeCompare(a.nama))
  } else if (urutan.value === 'stokBanyak') {
    hasil.sort((a, b) => b.stok - a.stok)
  } else if (urutan.value === 'stokSedikit') {
    hasil.sort((a, b) => a.stok - b.stok)
  }

  return hasil
})

// 4 Hitungan ringkasan (pakai computed)
const totalBarang = computed(() => daftarBarang.value.length)

const stokMenipisDanHabis = computed(() => {
  return daftarBarang.value.filter(b => b.stok <= 3).length
})

const jumlahKategori = computed(() => {
  const unik = new Set(daftarBarang.value.map(b => b.kategori))
  return unik.size
})

const totalUnit = computed(() => {
  return daftarBarang.value.reduce((jumlah, b) => jumlah + b.stok, 0)
})

// Tambah barang
const kirimBarang = async () => {
  if (!baru.value.nama || !baru.value.penanggung_jawab || !baru.value.kategori) {
    alert('Lengkapi semua data!')
    return
  }
  await fetch(ALAMAT, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(baru.value)
  })
  baru.value = { nama: '', penanggung_jawab: '', kategori: '', stok: 0 }
  await ambilData()
}

// Hapus barang
const hapusData = async (id) => {
  if (!confirm('Yakin ingin menghapus?')) return
  await fetch(`${ALAMAT}/${id}`, { method: 'DELETE' })
  await ambilData()
}

onMounted(ambilData)
</script>

<style scoped>
.wadah {
  max-width: 1200px;
  margin: 2rem auto;
  padding: 0 1rem;
  font-family: Arial, sans-serif;
}
h1 {
  text-align: center;
  color: #2c3e50;
}
.ringkasan {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1rem;
  margin-bottom: 1.5rem;
}
.kotak {
  background: #ecf0f1;
  padding: 1rem;
  border-radius: 8px;
  text-align: center;
}
.kotak h3 {
  margin: 0 0 0.5rem;
  font-size: 1rem;
  color: #34495e;
}
.kotak p {
  margin: 0;
  font-size: 1.5rem;
  font-weight: bold;
  color: #2980b9;
}
.kontrol {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1rem;
}
.kontrol input, .kontrol select {
  flex: 1;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
}
.form-tambah {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
}
.form-tambah input {
  flex: 1;
  min-width: 150px;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
}
button {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
.btn-tambah {
  background: #27ae60;
  color: white;
}
.btn-hapus {
  background: #e74c3c;
  color: white;
}
table {
  width: 100%;
  border-collapse: collapse;
}
th, td {
  padding: 0.75rem;
  text-align: left;
  border-bottom: 1px solid #ddd;
}
th {
  background: #f8f8f8;
}
.stok.aman { color: #27ae60; font-weight: bold; }
.stok.menipis { color: #f39c12; font-weight: bold; }
.stok.habis { color: #e74c3c; font-weight: bold; }
.badge {
  padding: 0.25rem 0.5rem;
  border-radius: 12px;
  font-size: 0.85rem;
  color: white;
}
.badge.aman { background: #27ae60; }
.badge.menipis { background: #f39c12; }
.badge.habis { background: #e74c3c; }
</style>