# trial1.py
import arena

def main():
    a = arena.Arena() #background_image = 'twoDots.png')
    a.add_key_car()
    rc = a.add_car()
    a.run_main_loop()

if __name__ == '__main__':
    main()
