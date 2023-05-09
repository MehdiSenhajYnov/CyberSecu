import os
import xml.etree.ElementTree as ET
from lxml import etree

def InitXML():
    if os.path.isfile('users.xml'):
        if not os.path.getsize('users.xml') > 0:
            root = ET.Element('users')
            tree = ET.ElementTree(root)
            tree.write('users.xml')
    else:
        root = ET.Element('users')
        tree = ET.ElementTree(root)
        tree.write('users.xml')

def save_user_to_xml(username, email, password):
    InitXML()
    # Créer un nouvel élément "user" dans l'arbre XML
    user = ET.Element("user")

    # Créer des sous-éléments pour stocker les informations de l'utilisateur
    username_element = ET.SubElement(user, "username")
    username_element.text = username
    email_element = ET.SubElement(user, "email")
    email_element.text = email
    password_element = ET.SubElement(user, "password")
    password_element.text = password
    role_element = ET.SubElement(user, "role")
    role_element.text = "user"

    # Charger l'arbre XML existant depuis le fichier s'il existe, sinon créer un nouvel arbre
    try:
        tree = ET.parse("users.xml")
        root = tree.getroot()
    except FileNotFoundError:
        root = ET.Element("users")
        tree = ET.ElementTree(root)

    # Ajouter le nouvel élément "user" à l'élément racine "users"
    root.append(user)
    tree.write("users.xml")

def userExist(username):
    try:
        tree = ET.parse('users.xml')
        root = tree.getroot()
    except:
        return False
    for user in root.findall('user'):
        if user.find('username').text == username:
            return True
    return False

def userExistEmail(email):
    try:
        tree = ET.parse('users.xml')
        root = tree.getroot()
    except:
        return False
    for user in root.findall('user'):
        if user.find('email').text == email:
            return True
    return False

def verify_credentials(email, password):
    # Charger le fichier XML
    tree = etree.parse("users.xml")

    try:
        xpath_query = "/users/user[email='" + str(email) + "' and password='" + str(password) + "']"
        # Exécuter la requête XPath
        result = tree.xpath(xpath_query)
    except Exception as e:
        return e
        
    if len(result) <= 0 :
        return False
    else:
        return True

def getUser(username):
    tree = etree.parse("users.xml")
    try:
        xpath_query = "/users/user[email='" + str(username) + "']"
        result = tree.xpath(xpath_query)
    except Exception as e:
        return e
    if len(result) <= 0 :
        return None
    else:
        return result[0]

def AccountToStr(account) -> str:
    strToReturn = ""
    if account is not None:
        strToReturn += account.find("username").text + "\n"
        strToReturn += account.find("email").text + "\n"
        strToReturn += account.find("password").text
    return strToReturn

def GetUsersBy(filterUser):
    tree = etree.parse("users.xml")
    try:
        xpath_query = "/users/user[starts-with(username, '" + filterUser +"')]/email"
        result = tree.xpath(xpath_query)
        strToReturn = ""
        for account in result:
            strToReturn += etree.tostring(account, encoding="unicode", pretty_print=True) + "\n"
        if len(result) > 0:
            return strToReturn
    except Exception as e:
        return e
