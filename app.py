from function import input_ip, input_validation
from menu import identificate, subnetting

print("")
print("================SISTEM IDENTIFIKASI IP ADDRESS v4================")
print("-----------------------------------------------------------------")
print("Sebelum memulai aplikasi, silahkan masukan IP Address yang ingin diidentifikasi terlebih dahulu")
ip_address = list()
ip_address = input_ip()


while True:
    print("============================== MENU ==============================")
    print(
        f"IP Address : {ip_address[0]}.{ip_address[1]}.{ip_address[2]}.{ip_address[3]} /{ip_address[4]}")
    print("1. Identifikasi IP Address")
    print("2. Subneting IP Address")
    print("3. Ganti IP yang ingin dioperasikan")
    print("0. Keluar aplikasi")
    menu = input("Pilih Menu : ")
    if menu == "1":
        identificate(ip_address)
    elif menu == "2":
        subnetting(ip_address)
    elif menu == "3":
        ip_address = input_ip()
    elif menu == "0":
        print("Terima Kasih...")
        break
    else:
        print("Menu tidak ada")
        continue

print("Selesai")
