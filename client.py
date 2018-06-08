from web_app import cli


def main():
	try:
		cli.main()
		print "Running server"
	except:
		print "Shutting down"


if __name__ == '__main__':
	main()
