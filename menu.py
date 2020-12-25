from function import detection, biner_prefix, biner_to_decimal, sum_subnet, blok_subnet, list_subnet, tabel_subnet, input_validation

# menu identifikasi


def identificate(oktet_ip):
    # mendeteksi kelas IP Address
    kelas = detection(oktet_ip)

    # mengkonversi prefix ke bentuk blok biner
    list_prefix_biner = []
    for x in range(0, 4):
        list_prefix_biner.append(biner_prefix(oktet_ip[4])[x])

    # mengkonversi prefix ke bentuk blok desimal
    list_prefix_desimal = []
    for x in range(0, 4):
        list_prefix_desimal.append(biner_to_decimal(list_prefix_biner[x]))

    # mencari jumlah subnetnya dan jumlah host per subnet
    jumlah_subnet = sum_subnet(kelas, list_prefix_biner)[0]
    jumlah_host = sum_subnet(kelas, list_prefix_biner)[1]

    # mencari blok subnet
    subnet_blok = blok_subnet(list_prefix_desimal, jumlah_subnet, kelas)

    # hasil subnetting nya
    print("\n=========================HASIL SCREENING=========================")
    print(
        f"IP Address\t\t : {oktet_ip[0]}.{oktet_ip[1]}.{oktet_ip[2]}.{oktet_ip[3]} /{oktet_ip[4]}")
    print(f"Kelas\t\t\t : {kelas}")
    print(
        f"Prefix Blok Biner\t : {list_prefix_biner[0]}.{list_prefix_biner[1]}.{list_prefix_biner[2]}.{list_prefix_biner[3]}")
    print(
        f"Prefix Blok Desimal\t : {list_prefix_desimal[0]}.{list_prefix_desimal[1]}.{list_prefix_desimal[2]}.{list_prefix_desimal[3]}")
    print(f"Jumlah Subnet\t\t : {jumlah_subnet}")
    print(f"Jumlah Host Tiap Subnet\t : {jumlah_host}")
    print(f"Blok Subnet\t\t : {subnet_blok}")
    print("=================================================================")


def subnetting(oktet_ip):
    result_subnet = []  # menampung subnet yang dihasilkan
    host_pertama = []  # menampung ip dari host pertama setiap subnet
    host_akhir = []  # menampung ip dari host terakhir setiap subnet
    ip_broadcast = []  # menampung ip dari ip broadcast setiap subnet

    # siapkan data yang dibutuhkan, yaitu blok subnet, kelas dan ip nya
    # mendeteksi kelas IP Address
    kelas = detection(oktet_ip)

    # mengkonversi prefix ke bentuk blok biner
    list_prefix_biner = []
    for x in range(0, 4):
        list_prefix_biner.append(biner_prefix(oktet_ip[4])[x])

    # mengkonversi prefix ke bentuk blok desimal
    list_prefix_desimal = []
    for x in range(0, 4):
        list_prefix_desimal.append(biner_to_decimal(list_prefix_biner[x]))

    # mencari jumlah subnetnya dan jumlah host per subnet
    jumlah_subnet = sum_subnet(kelas, list_prefix_biner)[0]
    # jumlah_host = sum_subnet(kelas, list_prefix_biner)[1]

    # mencari blok subnet
    subnet_blok = blok_subnet(list_prefix_desimal, jumlah_subnet, kelas)

    # cetak tabel subnetting nya
    print("\n\n===================================TABEL SUBNETTING===================================")
    print("No.\t | Subnet\t\t | Host Awal\t\t | Host Akhir\t\t | IP Broadscast")
    for x in range(0, len(subnet_blok)):
        if kelas == "A":
            oktet_ip[1] = subnet_blok[x]
            oktet_ip[2] = 0
            oktet_ip[3] = 0
            # untuk mengantisipasi out of range index nya, karena yang digunakan adalah 1 index lebih besar, maka pada perulangan terakhir ditulis manual 255
            if x == (len(subnet_blok)-1):
                ip_broadcast.append(f"{oktet_ip[0]}.255.255.255")
                host_akhir.append(f"{oktet_ip[0]}.255.255.254")
            else:
                ip_broadcast.append(
                    f"{oktet_ip[0]}.{subnet_blok[x+1]-1}.255.255")
                host_akhir.append(
                    f"{oktet_ip[0]}.{subnet_blok[x+1]-1}.255.254")

        elif kelas == "B":
            oktet_ip[2] = subnet_blok[x]
            oktet_ip[3] = 0
            # untuk mengantisipasi out of range index nya, karena yang digunakan adalah 1 index lebih besar, maka pada perulangan terakhir ditulis manual 255
            if x == (len(subnet_blok)-1):
                ip_broadcast.append(
                    f"{oktet_ip[0]}.{oktet_ip[1]}.255.255")
                host_akhir.append(
                    f"{oktet_ip[0]}.{oktet_ip[1]}.255.254")
            else:
                ip_broadcast.append(
                    f"{oktet_ip[0]}.{oktet_ip[1]}.{subnet_blok[x+1]-1}.255")
                host_akhir.append(
                    f"{oktet_ip[0]}.{oktet_ip[1]}.{subnet_blok[x+1]-1}.254")

        else:
            oktet_ip[3] = subnet_blok[x]
            if x == (len(subnet_blok)-1):
                ip_broadcast.append(
                    f"{oktet_ip[0]}.{oktet_ip[1]}.{oktet_ip[2]}.255")
                host_akhir.append(
                    f"{oktet_ip[0]}.{oktet_ip[1]}.{oktet_ip[2]}.254")
            else:
                ip_broadcast.append(
                    f"{oktet_ip[0]}.{oktet_ip[1]}.{oktet_ip[2]}.{subnet_blok[x+1]-1}")
                host_akhir.append(
                    f"{oktet_ip[0]}.{oktet_ip[1]}.{oktet_ip[2]}.{subnet_blok[x+1]-2}")

        result_subnet.append(
            f"{oktet_ip[0]}.{oktet_ip[1]}.{oktet_ip[2]}.{oktet_ip[3]}")
        host_pertama.append(
            f"{oktet_ip[0]}.{oktet_ip[1]}.{oktet_ip[2]}.{oktet_ip[3]+1}")

    for x in range(0, len(subnet_blok)):
        print(
            f"{x+1}.\t   {result_subnet[x]}\t\t   {host_pertama[x]}\t\t   {host_akhir[x]}\t\t   {ip_broadcast[x]}")
