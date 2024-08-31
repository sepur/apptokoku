from django.db import models
from django.contrib.auth.models import User


UKURAN_CHOICES = (('Pcs','Pcs'),('Renceng','Renceng'),('Bungkus','Bungkus'))
KATAGORI_CHOICES = (('1','Makanan'),('2','Minuman'))

STATUS_STOCK = (('1','Waiting'),('2','Approved'))
class Stok(models.Model):
    stok = models.IntegerField(blank=True,null=True)
    #ukuran = models.CharField(choices= UKURAN_CHOICES, max_length=500,null=True, blank=True)
    stok_barang = models.ForeignKey('Barang', on_delete=models.CASCADE)
    harga_beli = models.FloatField(null=True,blank=True)
    status = models.CharField(choices= STATUS_STOCK, max_length=500,null=True, blank=True)
    cu = models.ForeignKey(User, related_name='+', on_delete=models.CASCADE, editable=False, null=True, blank=True)
    mu = models.ForeignKey(User, related_name='+', on_delete=models.CASCADE, editable=False, null=True, blank=True)
    tanggal = models.DateField(null=True, blank=True)
    cdate = models.DateTimeField(auto_now_add=True)
    mdate = models.DateTimeField(auto_now=True)

    class Meta:
        db_table='stok'
        verbose_name = 'Stok'
        verbose_name_plural = verbose_name

    def total_harga_beli(self):
       return self.harga_beli * self.stok

    def total_stok_hitungan(self):
       return self.stok_barang.jumlah_stok + self.stok

class Barang(models.Model):
    nama_barang = models.CharField(max_length=500)
    kode_barang = models.CharField(max_length=500)
    ukuran = models.CharField(max_length=500)
    satuan = models.CharField(choices= UKURAN_CHOICES, max_length=500, null=True, blank=True)
    singkatan = models.CharField(max_length=500)
    katagori = models.CharField(choices= KATAGORI_CHOICES, max_length=500, null=True, blank=True)
    harga_barang = models.FloatField(null=True,blank=True)
    harga_jual = models.FloatField(null=True,blank=True)
    jumlah_stok = models.IntegerField(blank=True,null=True)
    cu = models.ForeignKey(User, related_name='+', on_delete=models.CASCADE, editable=False, null=True, blank=True)
    mu = models.ForeignKey(User, related_name='+', on_delete=models.CASCADE, editable=False, null=True, blank=True)
    cdate = models.DateTimeField(auto_now_add=True)
    mdate = models.DateTimeField(auto_now=True)

    class Meta:
        db_table='barang'
        verbose_name = 'Barang'
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s %s - %s - %s" %(self.nama_barang,self.ukuran,self.satuan,self.kode_barang,)


class PenjualanBarang(models.Model):
    nama_barang = models.CharField(max_length=500)
    kobar = models.ForeignKey(Barang, on_delete=models.CASCADE, null=True, blank=True)
    ukuran = models.CharField(max_length=500)
    satuan = models.CharField(choices= UKURAN_CHOICES, max_length=500, null=True, blank=True)
    singkatan = models.CharField(max_length=500)
    katagori = models.CharField(choices= KATAGORI_CHOICES, max_length=500, null=True, blank=True)
    harga_barang = models.FloatField(null=True,blank=True)
    harga_jual_langganan = models.FloatField(null=True,blank=True)
    harga_jual = models.FloatField(null=True,blank=True)
    cu = models.ForeignKey(User, related_name='+', on_delete=models.CASCADE, editable=False, null=True, blank=True)
    mu = models.ForeignKey(User, related_name='+', on_delete=models.CASCADE, editable=False, null=True, blank=True)
    cdate = models.DateTimeField(auto_now_add=True)
    mdate = models.DateTimeField(auto_now=True)
    isi = models.IntegerField(blank=True,null=True)

    class Meta:
        db_table='penjualanbarang'
        verbose_name = 'PenjualanBarang'
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s %s - %s - %s" %(self.nama_barang,self.ukuran,self.satuan,self.kobar,)


TIPE = (('1','Non Member'),('2','Member'))
class Pembeli(models.Model):
    nama = models.CharField(max_length=500)
    tipe_pembeli = models.CharField(choices= TIPE, max_length=500, null=True, blank=True)
    tgl_member = models.DateField(null=True, blank=True)
    cu = models.ForeignKey(User, related_name='+', on_delete=models.CASCADE, editable=False, null=True, blank=True)
    mu = models.ForeignKey(User, related_name='+', on_delete=models.CASCADE, editable=False, null=True, blank=True)
    cdate = models.DateTimeField(auto_now_add=True)
    mdate = models.DateTimeField(auto_now=True)

    class Meta:
        db_table='pembeli'
        verbose_name = 'Pembeli'
        verbose_name_plural = verbose_name

STS_BAYAR = (('1','BELUM'),('2','LUNAS'))
class Order(models.Model):
    pembeli = models.ForeignKey(Pembeli,related_name='+', on_delete=models.CASCADE)
    nominal_harus_dibayar = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
    nominal_pembayaran = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
    nominal_kembalian = models.DecimalField(max_digits=11, decimal_places=6, null=True, blank=True)
    total_barang = models.CharField(max_length=500)
    tanggal = models.DateField(null=True, blank=True)
    sts_bayar = models.CharField(choices= STS_BAYAR, max_length=500,null=True, blank=True)
    cu = models.ForeignKey(User, related_name='+', on_delete=models.CASCADE, editable=False, null=True, blank=True)
    mu = models.ForeignKey(User, related_name='+', on_delete=models.CASCADE, editable=False, null=True, blank=True)
    cdate = models.DateTimeField(auto_now_add=True)
    mdate = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table='order'
        verbose_name = 'Order'
        verbose_name_plural = verbose_name

class ItemOrder(models.Model):
    item_barang = models.ForeignKey(PenjualanBarang,related_name='+', on_delete=models.CASCADE)
    item_order = models.ForeignKey(Order,null=True, blank=True,related_name='+', on_delete=models.CASCADE)
    total_item = models.IntegerField(blank=True,null=True)
    harga_item = models.FloatField(null=True,blank=True)
    total_harga_item = models.FloatField(null=True,blank=True)
    diskon_item = models.CharField(max_length=500)
    ket_item = models.CharField(max_length=500)
    tanggal = models.DateField(null=True, blank=True)
    harga_barang = models.FloatField(null=True,blank=True)
    cu = models.ForeignKey(User, related_name='+', on_delete=models.CASCADE, editable=False, null=True, blank=True)
    mu = models.ForeignKey(User, related_name='+', on_delete=models.CASCADE, editable=False, null=True, blank=True)
    cdate = models.DateTimeField(auto_now_add=True)
    mdate = models.DateTimeField(auto_now=True)

    class Meta:
        db_table='itemorder'
        verbose_name = 'ItemOrder'
        verbose_name_plural = verbose_name

    #def total_harga_item(self):
       #return self.total_item * self.harga_item

    def total_harus_dibayar(self):
       return sum([self.total_harga_item])
