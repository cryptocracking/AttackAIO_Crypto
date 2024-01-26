#  ███╗    ███╗   ███╗███╗   ███╗██████╗ ██████╗ ███████╗ █████╗     ██████╗ ██████╗ ███╗   ███╗    ███╗ #
#  ██╔╝    ████╗ ████║████╗ ████║██╔══██╗██╔══██╗╚══███╔╝██╔══██╗   ██╔════╝██╔═══██╗████╗ ████║    ╚██║ #
#  ██║     ██╔████╔██║██╔████╔██║██║  ██║██████╔╝  ███╔╝ ███████║   ██║     ██║   ██║██╔████╔██║     ██║ #
#  ██║     ██║╚██╔╝██║██║╚██╔╝██║██║  ██║██╔══██╗ ███╔╝  ██╔══██║   ██║     ██║   ██║██║╚██╔╝██║     ██║ #
#  ███╗    ██║ ╚═╝ ██║██║ ╚═╝ ██║██████╔╝██║  ██║███████╗██║  ██║██╗╚██████╗╚██████╔╝██║ ╚═╝ ██║    ███║ #
#  ╚══╝    ╚═╝     ╚═╝╚═╝     ╚═╝╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝ ╚═════╝ ╚═════╝ ╚═╝     ╚═╝    ╚══╝ #
#   Programmer Mmdrza.Com ~ Telegram Channel @mPython3 ~ ID Telegram @PyMmdrza ~ https://Mmdrza.Com      #
##########################################################################################################



import codecs
import hashlib
import threading

import ecdsa
import requests
from hdwallet import HDWallet
from hdwallet.symbols import TRX as SYMBOL
from rich.console import Console
from rich.panel import Panel

console = Console()
console.clear()

filexname = input('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n [*] INSERT HERE File Name <---------|Without type file .txt|:::::::: ')

mylist = []

filename = str(filexname + ".txt")
with open(filename, newline='', encoding='utf-8') as f:
	for line in f:
		mylist.append(line.strip())


class BrainWallet:
	
	@staticmethod
	def generate_address_from_passphrase(passphrase):
		private_key = str(hashlib.sha256(
			passphrase.encode('utf-8')).hexdigest())
		address = BrainWallet.generate_address_from_private_key(private_key)
		return private_key, address
	
	@staticmethod
	def generate_address_from_private_key(private_key):
		public_key = BrainWallet.__private_to_public(private_key)
		address = BrainWallet.__public_to_address(public_key)
		return address
	
	@staticmethod
	def __private_to_public(private_key):
		private_key_bytes = codecs.decode(private_key, 'hex')
		key = ecdsa.SigningKey.from_string(
			private_key_bytes, curve=ecdsa.SECP256k1).verifying_key
		key_bytes = key.to_string()
		key_hex = codecs.encode(key_bytes, 'hex')
		bitcoin_byte = b'04'
		public_key = bitcoin_byte + key_hex
		return public_key
	
	@staticmethod
	def __public_to_address(public_key):
		public_key_bytes = codecs.decode(public_key, 'hex')
		# Run SHA256 for the public key
		sha256_bpk = hashlib.sha256(public_key_bytes)
		sha256_bpk_digest = sha256_bpk.digest()
		ripemd160_bpk = hashlib.new('ripemd160')
		ripemd160_bpk.update(sha256_bpk_digest)
		ripemd160_bpk_digest = ripemd160_bpk.digest()
		ripemd160_bpk_hex = codecs.encode(ripemd160_bpk_digest, 'hex')
		network_byte = b'00'
		network_bitcoin_public_key = network_byte + ripemd160_bpk_hex
		network_bitcoin_public_key_bytes = codecs.decode(
			network_bitcoin_public_key, 'hex')
		sha256_nbpk = hashlib.sha256(network_bitcoin_public_key_bytes)
		sha256_nbpk_digest = sha256_nbpk.digest()
		sha256_2_nbpk = hashlib.sha256(sha256_nbpk_digest)
		sha256_2_nbpk_digest = sha256_2_nbpk.digest()
		sha256_2_hex = codecs.encode(sha256_2_nbpk_digest, 'hex')
		checksum = sha256_2_hex[:8]
		address_hex = (network_bitcoin_public_key + checksum).decode('utf-8')
		wallet = BrainWallet.base58(address_hex)
		return wallet
	
	@staticmethod
	def base58(address_hex):
		alphabet = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
		b58_string = ''
		leading_zeros = len(address_hex) - len(address_hex.lstrip('0'))
		address_int = int(address_hex, 16)
		while address_int > 0:
			digit = address_int % 58
			digit_char = alphabet[digit]
			b58_string = digit_char + b58_string
			address_int //= 58
		ones = leading_zeros // 2
		for one in range(ones):
			b58_string = '1' + b58_string
		return b58_string


def balt(addr):
	block = requests.get("https://apilist.tronscan.org/api/account?address=" + addr)
	res = block.json()
	balances = dict(res)["balances"][0]["amount"]
	return balances


def MmDrza():
	w = 0
	count = 0
	
	for i in range(0, len(mylist)):
		count += 1
		passphrase = mylist[i]
		wallet = BrainWallet()
		private_key, address = wallet.generate_address_from_passphrase(passphrase)
		hdwallet: HDWallet = HDWallet(symbol=SYMBOL)
		hdwallet.from_private_key(private_key=private_key)
		addr = hdwallet.p2pkh_address()
		baltrx = balt(addr)
		MmdrzaPanel = str(
			'[gold1 on grey15]Total Checked: ' + '[orange_red1]' + str(count) + '[/][gold1 on grey15] ' + ' Win:' + '[white]' + str(w) + '[/][gold1]  BAL:[aquamarine1]' + str(baltrx) + '\n[/][gold1 on grey15]Addr: ' + '[white] ' + str(address) + '[gold1 on grey15]                  Passphrase: ' + '[orange_red1]' + str(passphrase) + '[/]\nPRIVATEKEY: [grey54]' + str(private_key) + '[/]')
		style = "gold1 on grey11"
		if float(baltrx) > 0:
			fx = open(u"TronBrain-" + str(filexname) + ".txt", "a")
			fx.write('\nAddress Compressed : ' + addr + '  Balance = ' + str(baltrx))
			fx.write('\nPassphrase       : ' + passphrase)
			fx.write('\nPrivate Key      : ' + private_key)
			fx.write('\nBalance: ' + str(val)
			fx.write('\n-------------- Programmer Steven----------------------\n')
			fx.close()
			console.print(Panel(str(MmdrzaPanel), title="[white]Win Wallet [/]", subtitle="[green_yellow blink] Mmdrza.Com [/]", style="red"), style=style, justify="full")
			w += 1
		else:
			console.print('[gold1]Total:[white]' + str(count) + '[/][gold1]-- Win:[white]' + str(w) + '[/][red1] TRON ADDR= [white on red1]' + str(addr) + '[/][blue] -------- BALANCE: [white]' + str(baltrx) + '[/][yellow]  Passphrase:[green]' + str(passphrase) + '[/]')


thr = threading.Thread(target=MmDrza)
thr.start()






# =====================================================
# DONATE (BTC) : 16p9y6EstGYcnofGNvUJMEGKiAWhAr1uR8
# Website : Mmdrza.Com
# Email : X4@mmdrza.Com
# Dev.to/Mmdrza
# Github.com/Pymmdrza
# =====================================================
