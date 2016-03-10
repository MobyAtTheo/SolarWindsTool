
all: 
	@echo "Perhaps you're looking to clean the .pyc files with 'make clean'?"
	@#echo "[+] Printing makefile"
	@#cat ./Makefile

clean:
	@echo -n Cleaning pyc files...
	@./dist_tools/clean_pyc.sh
	@echo done.
