import os
import subprocess
import random
import re
import shutil
import requests
import ctypes

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def generate_random_mac():
    mac = [0x00, 0x16, 0x3e, 
           random.randint(0x00, 0x7f),
           random.randint(0x00, 0xff),
           random.randint(0x00, 0xff)]
    return ':'.join(map(lambda x: "%02x" % x, mac))

def set_mac_address():
    print("Alterando endereço MAC do Ethernet...")
    adapter_name = "Ethernet"
    new_mac = generate_random_mac()
    print(f"Novo Mac: {new_mac}")
    # Regexp para verificar se o endereço MAC está no formato correto
    if not re.match(r'^([0-9a-f]{2}[:-]){5}([0-9a-f]{2})$', new_mac.lower()):
        raise ValueError("Endereço MAC inválido")

    # Converte o endereço MAC para o formato aceito pelo Windows (sem ':')
    new_mac = new_mac.replace(':', '')

    # Comando para alterar o endereço MAC no registro do Windows
    command = f'reg add "HKEY_LOCAL_MACHINE\\SYSTEM\\CurrentControlSet\\Control\\Class\\{{4d36e972-e325-11ce-bfc1-08002be10318}}\\0000" /v NetworkAddress /d {new_mac} /f'

    # Executa o comando
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"Erro ao alterar o endereço MAC: {result.stderr}")
    print("reiniciando adaptador Ethernet...")
    # Desabilita e habilita o adaptador de rede para aplicar a alteração
    subprocess.run(f'netsh interface set interface "{adapter_name}" disable', shell=True, capture_output=True)
    subprocess.run(f'netsh interface set interface "{adapter_name}" enable', shell=True, capture_output=True)

def anydesk_installed():
    if os.path.exists("C://Program Files (x86)//AnyDesk//anydesk.exe"):
        return "C://Program Files (x86)//AnyDesk"
    elif os.path.exists("C://Program Files//Anydesk/anydesk.exe"):
        return "C://Program Files//Anydesk"
    else:
        return False
    
def uninstall_anydesk():
    anydesk_path = anydesk_installed()
    if anydesk_path:
        print("Encontrado Anydesk instalado, realizando desinstalação...")
        comando = [anydesk_path+"//anydesk.exe", '--uninstall']
        # Executa o comando
        subprocess.run(comando, capture_output=True, text=True)
        print("Confirme a desinstalação do Anydesk!")

    else:
        print("Anydesk não está instalado, pulando desinstalação...")

def clean_files_anydesk():
    
    path_appdata = os.path.expandvars("%appdata%")+'\\Anydesk'
    print(f"limpando {path_appdata}")
    if os.path.isdir(path_appdata):
        try:
            # Remove o diretório e todo o seu conteúdo
            shutil.rmtree(path_appdata)
            print(f"Diretório {path_appdata} e todo o seu conteúdo foram removidos.")

        except Exception as e:
            print(f"Erro ao tentar remover o diretório {path_appdata}. Motivo: {e}")

def download_anydesk(url,download_dir):
    
    local_filename = os.path.join(download_dir, 'Anydesk.exe')
    if os.path.exists(local_filename):
        return local_filename
    
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    
    print('baixado Anydesk.exe na área de trabalho')

    return local_filename

def main():
    if not is_admin():
        input("Abra como Administrador!")
    else:
        uninstall_anydesk()
        clean_files_anydesk()
        local_filename = download_anydesk('https://download.anydesk.com/AnyDesk.exe',f'{os.path.expandvars("%USERPROFILE%")}\\Desktop')
        set_mac_address()
        os.startfile(local_filename)

main()