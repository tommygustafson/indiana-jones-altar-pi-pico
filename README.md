# Indiana Jones - Fertility Idol Altar
This is the code that connects the PN532 RFID reader, activates the linear actuator and can also communicate with other devices with ESP322 radio

- Pi zero -> runs altar.py which drives the PN532 RFID reader, controls linear actuator and sends commands to other devices with ESP322 radio
- Pi 3 -> runs listen-act.py, which receives the RFID key tag string via ESP322 and can then act based on this tag

- Git commit -am “commit notes”
- Git push origin main   # pushes changes on pi’s to GitHub
- Git pull origin main  # pulls or gets files from Github to pi

- BIG CHANGES!!!!!
