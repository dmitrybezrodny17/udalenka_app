from modules.scrapers import djinni, rabota, work, grc

def main():
	djinni.get_urls()
	rabota.get_urls()
	grc.get_urls()
	work.get_urls()

if __name__ == '__main__':
	main()