import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from api.config import Config

def envoyer_email_client(email_client, code_commande, mot_de_passe):
    """
    Envoie un email au client avec son code de commande et mot de passe
    
    Args:
        email_client (str): Email du client
        code_commande (str): Code de la commande
        mot_de_passe (str): Mot de passe pour ouvrir le casier
    
    Returns:
        bool: True si envoi réussi, False sinon
    """
    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = f"Votre colis est disponible - Code: {code_commande}"
        msg['From'] = Config.SMTP_USERNAME
        msg['To'] = email_client
        
        text = f"""
Bonjour,

Votre colis est maintenant disponible dans le casier de livraison !

Pour récupérer votre commande :
1. Rendez-vous au locker (parking du centre-ville)
2. Sur l'écran tactile, entrez les informations suivantes :

   Code de commande : {code_commande}
   Mot de passe     : {mot_de_passe}

3. Le casier s'ouvrira automatiquement

⚠️ Conservez bien ces codes, ils sont nécessaires pour récupérer votre colis.

Cordialement,
L'équipe Locker
        """
        
        html = f"""
<html>
  <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
    <h2 style="color: #2c3e50;">🎉 Votre colis est disponible !</h2>
    
    <p>Bonjour,</p>
    
    <p>Votre colis est maintenant disponible dans le casier de livraison.</p>
    
    <div style="background-color: #f8f9fa; padding: 20px; border-radius: 5px; margin: 20px 0;">
      <h3 style="margin-top: 0; color: #2c3e50;">📦 Informations de retrait</h3>
      <p><strong>Code de commande :</strong> <span style="font-size: 18px; color: #e74c3c;">{code_commande}</span></p>
      <p><strong>Mot de passe :</strong> <span style="font-size: 18px; color: #e74c3c;">{mot_de_passe}</span></p>
    </div>
    
    <h3>Comment récupérer votre colis ?</h3>
    <ol>
      <li>Rendez-vous au locker (parking du centre-ville)</li>
      <li>Sur l'écran tactile, entrez votre code de commande et mot de passe</li>
      <li>Le casier s'ouvrira automatiquement</li>
    </ol>
    
    <p style="color: #e74c3c;"><strong>⚠️ Conservez bien ces codes !</strong></p>
    
    <p>Cordialement,<br>L'équipe Locker</p>
  </body>
</html>
        """
        
        part1 = MIMEText(text, 'plain')
        part2 = MIMEText(html, 'html')
        
        msg.attach(part1)
        msg.attach(part2)
        
        server = smtplib.SMTP(Config.SMTP_SERVER, Config.SMTP_PORT)
        server.starttls()
        server.login(Config.SMTP_USERNAME, Config.SMTP_PASSWORD)
        server.send_message(msg)
        server.quit()
        
        print(f"✅ Email envoyé à {email_client}")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de l'envoi de l'email: {e}")
        return False
