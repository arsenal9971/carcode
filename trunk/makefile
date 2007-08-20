# carcode archive makefile

# macros
ZIP = zip
ARCHIVE = archive.zip
PY = trial1.py arena.py car.py
MISC = readme.txt
DATA_DIR = data
PNG = $(DATA_DIR)/*.png
WAV = $(DATA_DIR)/*.wav

# rules
archive: $(ARCHIVE)

# -u option updates files in the archive
# -x option ensures the data/.svn folder is not archived
$(ARCHIVE): $(PY) $(MISC) $(PNG) $(WAV)
	$(ZIP) -u $(ARCHIVE) $(PY) $(MISC) $(PNG) $(WAV) #-x data/.svn

# - means to ignore errors
# @ prevents echoing
# -f prevents confirmation prompting
clean:
	-@rm -f *.pyc