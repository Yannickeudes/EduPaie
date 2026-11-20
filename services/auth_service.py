import hashlib
import secrets


ROLES = ("Directeur", "Comptable", "Secrétaire")
LONGUEUR_MIN_MOT_DE_PASSE = 4


class AuthService:
    def __init__(self, utilisateur_repository):
        self.utilisateur_repository = utilisateur_repository

    @staticmethod
    def _hacher(mot_de_passe, sel):
        if isinstance(sel, str):
            sel = sel.encode("utf-8")

        return hashlib.pbkdf2_hmac(
            "sha256",
            mot_de_passe.encode("utf-8"),
            sel,
            100_000
        ).hex()

    def comptes_configures(self):
        return (
            self.utilisateur_repository.compter()
            >= len(ROLES)
        )

    def configurer_comptes(self, mots_de_passe):
        for role in ROLES:
            mot_de_passe = mots_de_passe.get(role, "")

            self._valider_mot_de_passe(mot_de_passe)

        for role in ROLES:
            mot_de_passe = mots_de_passe[role]

            sel = secrets.token_hex(16)

            self.utilisateur_repository.ajouter(
                role,
                role,
                self._hacher(mot_de_passe, sel),
                sel
            )

    def verifier(self, role, mot_de_passe):
        utilisateur = (
            self.utilisateur_repository
            .trouver_par_role(role)
        )

        if utilisateur is None:
            return False

        hash_attendu = utilisateur[3]
        sel = utilisateur[4]

        hash_fourni = self._hacher(
            mot_de_passe,
            sel
        )

        return secrets.compare_digest(
            hash_fourni,
            hash_attendu
        )

    def changer_mot_de_passe(
        self,
        role,
        mot_de_passe_actuel,
        nouveau_mot_de_passe
    ):
        if not self.verifier(role, mot_de_passe_actuel):
            raise ValueError(
                "Le mot de passe actuel est incorrect."
            )

        self._valider_mot_de_passe(nouveau_mot_de_passe)

        sel = secrets.token_hex(16)

        self.utilisateur_repository.mettre_a_jour_mot_de_passe(
            role,
            self._hacher(nouveau_mot_de_passe, sel),
            sel
        )

    @staticmethod
    def _valider_mot_de_passe(mot_de_passe):
        if len(mot_de_passe) < LONGUEUR_MIN_MOT_DE_PASSE:
            raise ValueError(
                "Le mot de passe doit contenir au moins "
                f"{LONGUEUR_MIN_MOT_DE_PASSE} caractères."
            )
