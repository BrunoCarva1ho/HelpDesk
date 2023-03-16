import matplotlib.pyplot as plt
from bd import mysql

def grafico():
    with mysql.cursor() as cur:
        cur.execute("SELECT intensidade FROM relato")
        intensidade = cur.fetchall()

    # Intensidades
    i1 = 0
    i2 = 0
    i3 = 0
    i4 = 0
    i5 = 0

    for x in intensidade:
        if x == (1,):
            i1 = i1+1

        elif x == (2,):
            i2 = i2 + 1

        elif x == (3,):
            i3 = i3 + 1

        elif x == (4,):
            i4 = i4 + 1

        elif x == (5,):
            i5 = i5 + 1

    labels = ['1', '2', '3', '4', '5']

    vals = [i1,
            i2,
            i3,
            i4,
            i5]
    
    print(intensidade)
    print(vals)
    fig, ax = plt.subplots(figsize=(10, 4))

    ax.pie(vals, labels=labels, autopct="%.2f%%")
    
    ax.set_title( ('Gráfico das intensidades:') , fontsize=16)

    plt.savefig("./static/graf/pizza.png", transparent=True)
