from django.contrib import admin
from .models import Stok, Barang, Pembeli, Order, ItemOrder,PenjualanBarang
from import_export.admin import ImportExportMixin, ExportActionModelAdmin


class PenjualanBarangAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['id','kobar','nama_barang','harga_barang','harga_jual_langganan','harga_jual','isi']
    search_fields = ['id','kobar','nama_barang','harga_barang','harga_jual_langganan','harga_jual','isi']
admin.site.register(PenjualanBarang,PenjualanBarangAdmin)

class StokAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['id','stok','stok_barang']
    search_fields = ['id','stok','stok_barang']
admin.site.register(Stok,StokAdmin)

class BarangAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['id','kode_barang','nama_barang','ukuran','jumlah_stok']
    search_fields = ['id','kode_barang','nama_barang','jumlah_stok']
admin.site.register(Barang,BarangAdmin)

class PembeliAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['id','nama','tipe_pembeli','tgl_member']
    search_fields = ['id','nama','tipe_pembeli','tgl_member']
admin.site.register(Pembeli,PembeliAdmin)


class OrderAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['id','pembeli','nominal_harus_dibayar','nominal_pembayaran','nominal_kembalian','total_barang','tanggal']
    search_fields = ['id','pembeli','nominal_harus_dibayar','nominal_pembayaran','nominal_kembalian','total_barang','tanggal']
admin.site.register(Order,OrderAdmin)

class ItemOrderAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['id','item_barang','item_order','total_item','harga_item','diskon_item']
    search_fields = ['id','item_barang','item_order','total_item','harga_item','diskon_item']
admin.site.register(ItemOrder,ItemOrderAdmin)


