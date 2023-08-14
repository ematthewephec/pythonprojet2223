import os
import hashlib
from pykeepass import PyKeePass, create_database


def my_pass():
    exist = False
    name_user_crypt=""#def variable nom user crypté
    name_user = input("entrer le nom de votre user") #input nom user connexion et inscription
    mdp_user = input("entrer un mot de passe maitre pour votre user") # choix du mot de passe ou vérification mot de passe
    indice_user = input("entrer votre indice en cas d'oubli de votre mot de passe maitre")# choix indice mot de passe maitre
    print("votre nom est " + name_user + " votre mot de passe est maitre " + mdp_user + " votre indice est " + indice_user)
    result = hashlib.md5(name_user.encode()) 
    print("The hexadecimal equivalent of hash is : ", end ="")#affichage du hash en console
    print(result.hexdigest())
    basepath = ('./pass') #emplacement du stockage des fichiers (il faut creer un dossier pass)
    for entry in os.listdir(basepath):# parcours les fichiers verifier que l'user n'existe pas. 
        if os.path.isfile(os.path.join(basepath, entry)):
            print(entry)
            print(result.hexdigest())
            print(entry.replace(".kdbx",""))
            if (entry.replace(".kdbx","")==result.hexdigest()):
                print("user déja existant")
                exist = True
                name_user_crypt = str(result.hexdigest())
    
    if (exist):
        print("ouverture du fichier")
        filename="./pass/"+ str(result.hexdigest()) + ".kdbx"
        kp = PyKeePass(filename, password=mdp_user)
        choice= input("a pour ajouter un mdp et d pour afficher les mots de passes")
        if (choice=="a"):
            nomduservice= input("entrer le nom du service")
            nomduser=input("entrer le nom user du service / du site web")
            mdpservice =input ("entrer le MDP du service") 
            kp.add_entry(kp.root_group, nomduservice, nomduser, mdpservice)
            kp.save()
        elif(choice=="d"):
            nomduservice= input("entrer le nom du service")
            entry = kp.find_entries(title= nomduservice, first=True)
            print(entry.password)

    else:
        print("création du user")
        filename="./pass/"+ str(result.hexdigest()) + ".kdbx"
        print(filename)
        create_database(filename, password=mdp_user, keyfile=None, transformed_key=None)


      
