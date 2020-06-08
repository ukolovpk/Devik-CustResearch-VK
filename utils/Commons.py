from datetime import date 


class Commons(object):

    def calculateAge(self, birthDate): 
        today = date.today() 
        age = today.year - birthDate.year - ((today.month, today.day) < (birthDate.month, birthDate.day)) 
        return age 
