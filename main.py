from interpolacion import Interpolacion, db_config

def main():
    
    interpolator = Interpolacion(db_config())

    lambda1 = 1.2644
    bi = interpolator.get_bi_given_lambda1(lambda1)

    print(lambda1,bi)

if __name__ == "__main__":
    main()
