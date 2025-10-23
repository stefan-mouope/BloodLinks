from django.core.exceptions import ValidationError

def verifier_code_doc(code):
    if not code.endswith("DOC"):
        raise ValidationError("Le code n'est pas valide pour un docteur.")

def verifier_code_banc(code):
    if not code.endswith("BANC"):
        raise ValidationError("Le code n'est pas valide pour une banque.")