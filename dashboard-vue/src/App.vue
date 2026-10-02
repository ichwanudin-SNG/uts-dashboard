<template>
  <div class="container">
    <h1>📋 Daftar Barang Inventaris</h1>

    <div class="cards">
      <div class="card">
        <h3>Total Barang</h3>
        <p>{{ totalBarang }}</p>
      </div>
      <div class="card">
        <h3>Stok Menipis + Habis</h3>
        <p>{{ stokMenipis }}</p>
      </div>
      <div class="card">
        <h3>Jumlah Kategori</h3>
        <p>{{ jumlahKategori }}</p>
      </div>
      <div class="card">
        <h3>Total Unit</h3>
        <p>{{ totalUnit }}</p>
      </div>
    </div>

    <div class="controls">
      <input v-model="kataKunci" placeholder="Cari nama barang / penanggung jawab..." />
      <select v-model="urutan">
        <option value="">Urutkan...</option>
        <option value="nama">Nama A–Z</option>
        <option value="-stok">Stok Terbanyak</option>
        <option value="stok">Stok Tersedikit</option>
      </select>
    </div>

    <div class="form-tambah">
      <input v-model="barangBaru.nama" placeholder="Nama Barang" />
      <input v-model="barangBaru.penanggung_jawab" placeholder="Penanggung Jawab" />
      <input v-model="barangBaru.kategori" placeholder="Kategori" />
      <input v-model.number="barangBaru.stok" type="number" placeholder="Stok" />
      <button @click="tambahBarang" class="btn-tambah">+ Tambah</button>
    </div>

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
        <tr v-for="b in barangTerfilter" :key="b.id">
          <td>{{ b.nama }}</td>
          <td>{{ b.penanggung_jawab }}</td>
          <td>{{ b.kategori }}</td>
          <td :class="{ rendah: b.stok <= 3, sedang: b.stok <= 5 && b.stok > 3 }">{{ b.stok }}</td>
          <td>
            <span v-if="b.stok > 5" class="status aman">Aman</span>
            <span v-else-if="b.stok > 0 && b.stok <= 5" class="status menipis">Menipis</span>
            <span v-else class="status habis">Habis</span>
          </td>
          <td><button @click="hapusBarang(b.id)" class="btn-hapus">Hapus</button></td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

const ALAMAT_API = 'http://127.0.0.1:8000/barang'

const daftarBarang = ref([])
const kataKunci = ref('')
const urutan = ref('')
const barangBaru = ref({ nama: '', penanggung_jawab: '', kategori: '', stok: 0 })

const muatData = async () => {
  try {
    const res = await fetch(ALAMAT_API)
    daftarBarang.value = await res.json()
  } catch {
    alert('Gagal ambil data! Pastikan backend menyala di ' + ALAMAT_API)
  }
}

const tambahBarang = async () => {
  if (!barangBaru.value.nama) return
  await fetch(ALAMAT_API, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(barangBaru.value)
  })
  barangBaru.value = { nama: '', penanggung_jawab: '', kategori: '', stok: 0 }
  await muatData()
}

const hapusBarang = async (id) => {
  await fetch(`${ALAMAT_API}/${id}`, { method: 'DELETE' })
  await muatData()
}

const barangTerfilter = computed(() => {
  let hasil = daftarBarang.value.filter(b =>
    b.nama.includes(kataKunci.value) || b.penanggung_jawab.includes(kataKunci.value)
  )
  if (urutan.value === 'nama') hasil.sort((a, b) => a.nama.localeCompare(b.nama))
  if (urutan.value === 'stok') hasil.sort((a, b) => a.stok - b.stok)
  if (urutan.value === '-stok') hasil.sort((a, b) => b.stok - a.stok)
  return hasil
})

const totalBarang = computed(() => daftarBarang.value.length)
const stokMenipis = computed(() => daftarBarang.value.filter(b => b.stok <= 5).length)
const jumlahKategori = computed(() => new Set(daftarBarang.value.map(b => b.kategori)).size)
const totalUnit = computed(() => daftarBarang.value.reduce((j, b) => j + b.stok, 0))

onMounted(muatData)
</script>

<style scoped>
.container { max-width: 1400px; margin: 0 auto; padding: 20px; font-family: Arial, sans-serif; }
h1 { text-align: center; color: #2c3e50; margin-bottom: 30px; }
.cards { display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; margin-bottom: 25px; }
.card { background: #ecf0f1; padding: 20px; border-radius: 8px; text-align: center; }
.card h3 { margin: 0 0 10px; font-size: 16px; color: #34495e; }
.card p { font-size: 28px; font-weight: bold; margin: 0; color: #2980b9; }
.controls { display: flex; gap: 10px; margin-bottom: 15px; }
.controls input { flex: 1; padding: 10px; border: 1px solid #ddd; border-radius: 4px; }
.controls select { padding: 10px; border: 1px solid #ddd; border-radius: 4px; }
.form-tambah { display: flex; gap: 8px; margin-bottom: 20px; }
.form-tambah input { flex: 1; padding: 10px; border: 1px solid #ddd; border-radius: 4px; }
.btn-tambah { background: #27ae60; color: white; border: none; padding: 10px 20px; border-radius: 4px; cursor: pointer; }
table { width: 100%; border-collapse: collapse; background: white; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
th, td { padding: 12px 15px; text-align: left; border-bottom: 1px solid #eee; }
th { background: #f8f8f8; font-weight: bold; }
.rendah { color: #e74c3c; font-weight: bold; }
.sedang { color: #f39c12; }
.status { padding: 4px 10px; border-radius: 12px; font-size: 13px; }
.aman { background: #d4edda; color: #155724; }
.menipis { background: #fff3cd; color: #856404; }
.habis { background: #f8d7da; color: #721c24; }
.btn-hapus { background: #e74c3c; color: white; border: none; padding: 6px 12px; border-radius: 4px; cursor: pointer; }
</style>