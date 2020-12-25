# fungsi untuk input data ip address
def input_ip():
    on = 1  # membatasi iterasi
    oktet_ip = list()  # menyimpan oktet 1-4 di index 0-3 dan prefix di index 4
    validasi = list()  # menyimpan kondisi validasi range dan integer
    while on < 6:
        kondisi = False
        while kondisi == False:
            # jika sudah sampai iterasi 5, maka input prefix, bukan oktet desimal lagi
            if on == 5:
                error = "Nilai prefix hanya berisi 8-32 saja"
                nilai = input(f"Masukan nilai prefix : ")
            elif on == 1:
                error = "Nilai oktet pertama harus berisi 1-255 dan tidak boleh 127"
                nilai = input(f"Masukan nilai desimal oktet ke-{on} : ")
            else:
                error = "Nilai oktet kedua, ketiga dan keempat harus berisi 0-255"
                nilai = input(f"Masukan nilai desimal oktet ke-{on} : ")

            validasi = input_validation(nilai, on)
            if validasi[0] == False:
                print("Nilai harus angka")
            elif validasi[1] == False:
                print(error)
            else:
                oktet_ip.append(int(nilai))
                on += 1
                kondisi = True
    return oktet_ip

# fungsi untuk validasi input


def input_validation(nilai, iterasi):
    # index 1 menampung validasi range angka, index 0 validasi integer
    result = [True, True]
    isi = nilai
    if isi.isdigit():
        # jika iterasi ke 5, maka ceknya ganti ke prefix, bukan oktet lagi
        if iterasi == 5:
            batas_atas = 32
            batas_bawah = 8
        elif iterasi == 1:
            batas_atas = 255
            batas_bawah = 1
        else:
            batas_atas = 255
            batas_bawah = 0

        if iterasi == 1:  # pada iterasi pertama, validasi oktet pertama tidak boleh 127
            if int(isi) != 127 and batas_bawah <= int(isi) <= batas_atas:
                result[1] = True
                return result
            else:
                result[1] = False
        else:  # pada iterasi lainnnya, validasi oktet lainnya boleh 127
            if batas_bawah <= int(isi) <= batas_atas:
                result[1] = True
                return result
            else:
                result[1] = False

    else:
        result[0] = False
    return result


# fungsi untuk mencari tahu kelas IP Address
def detection(ip):
    detect_result = ["", ""]
    if int(ip[0]) <= 126 and int(ip[0]) >= 1:
        detect_result[0] = "A"
    elif int(ip[0]) <= 191 and int(ip[0]) >= 128:
        detect_result[0] = "B"
    elif int(ip[0]) <= 223 and int(ip[0]) >= 192:
        detect_result[0] = "C"
    elif int(ip[0]) <= 239 and int(ip[0]) >= 224:
        detect_result[0] = "D"
    else:
        detect_result[0] = "E"

    return detect_result[0]


# fungsi untuk mengubah prefix desimal benjadi blok biner
def biner_prefix(prefix):
    biner = ""
    x = 1
    while x <= prefix:
        biner += "1"
        x += 1

    # mendapatkan sisa prefix dari IPv4, total maks prefixnya adalah 32
    sisa_prefix = 32-prefix
    # list untuk menampung biner tiap blok
    hasil = []
    # cek apakah jumlah prefix nya 32, jika iya maka proses berhenti dan tampilkan prefix biner nya
    kondisi = False
    while kondisi == False:
        if sisa_prefix == 0:
            kondisi = True
        else:
            # tambahkan biner 0 sebanyak sisa kekurangan prefix agar lengkap menjadi 32 bit
            for x in range(1, sisa_prefix+1):
                biner += "0"

            # pecah biner yang dihasilkan setiap 8 karakter dan masukan ke list hasil
            hasil.append(biner[0:8])
            hasil.append(biner[8:16])
            hasil.append(biner[16:24])
            hasil.append(biner[24:32])
            kondisi = True
    # kembalikan variabel hasil
    return hasil


# fungsi untuk merubah biner ke desimal
def biner_to_decimal(biner):
    desimal = 0
    x = 7
    i = 0
    while x >= 0:
        desimal += 2**i * int(biner[x])
        x -= 1
        i += 1
    return desimal


# fungsi untuk mencari jumlah subnet
def sum_subnet(kelas, biner):
    full_biner = ""
    # menjadikan list prefix binner jadi satu string utuh
    for x in range(0, 4):
        full_biner += biner[x]

    # memfilter biner yang digunakan perhitungan berdasarkan kelas
    if kelas == "A":
        used_biner = full_biner[8:32]
    elif kelas == "B":
        used_biner = full_biner[16:32]
    else:
        used_biner = full_biner[24:32]

    # mencari jumlah biner 1 dan 0
    one = 0
    zero = 0
    for x in range(0, len(used_biner)):
        if used_biner[x] == "1":
            one += 1
        else:
            zero += 1

    # menghitung jumlah subnet dan host subnet nya
    subnet = 2 ** one
    host_subnet = 2 ** zero-2

    return subnet, host_subnet


# fungsi untuk mencari blok subnet
def blok_subnet(prefix_desimal, jumlah_subnet, kelas):
    list_subnet = []

    if kelas == "A":
        blok_subnet = 256 - int(prefix_desimal[1])
    elif kelas == "B":
        blok_subnet = 256 - int(prefix_desimal[2])
    else:
        blok_subnet = 256 - int(prefix_desimal[3])

    i = 0
    x = 0
    while x < jumlah_subnet:
        list_subnet.append(i)
        i += blok_subnet
        x += 1

    return list_subnet


# fungsi untuk membuat list hasil subnet
def list_subnet(blok_subnet, list_ip, kelas):
    result_subnet = []
    for x in range(0, len(blok_subnet)):
        if kelas == "A":
            list_ip[1] = blok_subnet[x]
            list_ip[2] = 0
            list_ip[3] = 0
        elif kelas == "B":
            list_ip[2] = blok_subnet[x]
            list_ip[3] = 0
        else:
            list_ip[3] = blok_subnet[x]
        result_subnet.append(
            f"{list_ip[0]}.{list_ip[1]}.{list_ip[2]}.{list_ip[3]}")

    return result_subnet


# fungsi untuk membuat tabel hasil subnetting
def tabel_subnet(blok_subnet, kelas, list_ip):
    result_subnet = []
    host_pertama = []
    host_akhir = []
    ip_broadcast = []
    for x in range(0, len(blok_subnet)):
        if kelas == "A":
            list_ip[1] = blok_subnet[x]
            list_ip[2] = 0
            list_ip[3] = 0
            # untuk mengantisipasi out of range index nya, karena yang digunakan adalah 1 index lebih besar, maka pada perulangan terakhir ditulis manual 255
            if x == (len(blok_subnet)-1):
                ip_broadcast.append(f"{list_ip[0]}.255.255.255")
                host_akhir.append(f"{list_ip[0]}.255.255.254")
            else:
                ip_broadcast.append(
                    f"{list_ip[0]}.{blok_subnet[x+1]-1}.255.255")
                host_akhir.append(f"{list_ip[0]}.{blok_subnet[x+1]-1}.255.254")

        elif kelas == "B":
            list_ip[2] = blok_subnet[x]
            list_ip[3] = 0
            # untuk mengantisipasi out of range index nya, karena yang digunakan adalah 1 index lebih besar, maka pada perulangan terakhir ditulis manual 255
            if x == (len(blok_subnet)-1):
                ip_broadcast.append(
                    f"{list_ip[0]}.{list_ip[1]}.255.255")
                host_akhir.append(
                    f"{list_ip[0]}.{list_ip[1]}.255.254")
            else:
                ip_broadcast.append(
                    f"{list_ip[0]}.{list_ip[1]}.{blok_subnet[x+1]-1}.255")
                host_akhir.append(
                    f"{list_ip[0]}.{list_ip[1]}.{blok_subnet[x+1]-1}.254")

        else:
            list_ip[3] = blok_subnet[x]
            if x == (len(blok_subnet)-1):
                ip_broadcast.append(
                    f"{list_ip[0]}.{list_ip[1]}.{list_ip[2]}.255")
                host_akhir.append(
                    f"{list_ip[0]}.{list_ip[1]}.{list_ip[2]}.254")
            else:
                ip_broadcast.append(
                    f"{list_ip[0]}.{list_ip[1]}.{list_ip[2]}.{blok_subnet[x+1]-1}")
                host_akhir.append(
                    f"{list_ip[0]}.{list_ip[1]}.{list_ip[2]}.{blok_subnet[x+1]-2}")

        result_subnet.append(
            f"{list_ip[0]}.{list_ip[1]}.{list_ip[2]}.{list_ip[3]}")
        host_pertama.append(
            f"{list_ip[0]}.{list_ip[1]}.{list_ip[2]}.{list_ip[3]+1}")

    for x in range(0, len(blok_subnet)):
        print(
            f"{x+1}.\t   {result_subnet[x]}\t   {host_pertama[x]}\t   {host_akhir[x]}\t   {ip_broadcast[x]}")
