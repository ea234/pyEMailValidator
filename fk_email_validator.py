def validateEmail( pEingabe = '' ):

    '''Validiert eine eMail-Adresse'''   
    
    fkt_ergebnis = 0
   
    # 
    # Pruefung: Eingabelaenge gleich 0 ?
    #
    # Es wird kein Trim gemacht, da ein Trim Zeit verbrauchen wuerde.
    # Diese Funktion soll den String so pruefen, wie dieser uebergeben wurde.
    # Es ist nicht die Aufgabe dieser Funktion, die Eingabe zu manipulieren.
    # Besteht die Eingabe nur aus Leerzeichen, wird beim ersten Leerzeichen
    # ein ungueltiges Zeichen erkannt und der Fehler 29 zurueckgegeben.
    #
    # Ist die Eingabe ohne Trim schon ein Leerstring, wird der
    # Fehler 11 zurueckgegeben.
    # 
    
    if ( len( pEingabe ) == 0 ):
        return 10
   
    #
    # Laenge Eingabestring
    # Die Variable "laenge_eingabe_string" bezeichnete in der ersten Version 
    # die tatsaechliche Laenge des Eingabestrings. Durch den Einbau der Pruefroutine
    # fuer eckige Klammern, kann der Inhalt aber auch die Bedeutung einer 
    # Positonsangabe haben. 
    #
    laenge_eingabe_string = len( pEingabe )

    #
    # Generell darf die Eingabe nicht laenger als 255 Zeichen sein.
    # Die Pruefung auf die minimale Laenge der eMail-Adresse folgt weiter unten.
    #
    if ( laenge_eingabe_string > 255 ):
        return 12
    
    # 
    #Position AT-Zeichen
    #Initialwert -1 steht fuer "kein AT-Zeichen gefunden"
    # 
    position_at_zeichen = -1

    # 
    #Merker "letzte Position eines Punktes"
    #Initialwert -1 steht fuer "keinen Punkt gefunden"
    # 
    position_letzter_punkt = -1

    # 
    #Speichert die Position des zuletzt gefundenen Anfuehrungszeichens. 
    #Start- oder Endzeichen. 
    # 
    position_anf_zeichen_akt = -1

    # 
    #Speichert die Position der letzten geschlossenen Klammer ')' eines gueltigen Kommentares. 
    # 
    position_kommentar_ende = -1

    position_kommentar_start = -1

    # 
    #Zaehler fuer Zeichen zwischen zwei Trennzeichen.
    #Die Trennzeichen sind Punkt und AT-Zeichen
    # 
    zeichen_zaehler = 0

    # 
    #Start Leseposition
    #Die Startposition fuer die While-Schleife ist hier 0. Das ist
    #das erste Zeichen der Eingabe. 
    #
    #Bei eMail-Adressen in spitzen Klammern ist die Startposition 
    #immer die Position nach der oeffnenden eckigen Klammer.
    # 
    akt_index = 0

    aktuelles_zeichen = ' '

    # 
    #Pruefung: Eckige Klammern
    #
    #Rudimentaer eingebaut
    #   
    # ABC DEF <ABC.DEF@GHI.JKL>
    #
    # <ABC.DEF@GHI.JKL> ABC DEF
    #
    # Startet die eMail-Adresse mit einer oeffnenden eckigen Klammer, wird 
    # eine schliessende eckige Klammmer gesucht. Von vorne nach hinten.
    #
    # Ende die eMail-Adresse mit einer schliessenden eckigen Klammer, wird 
    # eine oeffnende eckige Klammer gesucht. Von hinten nach vorne.
    #
    # Wird keine korrospondierende Klammer gefunden, wird die Funktion 
    # mit einem Fehlercode (16 oder 17) beendet.
    #
    # Wird die korrospondierende Klammer gefunden, wird die Start- und 
    # Endposition fuer die eigentliche Pruefroutine auf die in den 
    # eckigen Klammern enthaltende eMail-Adresse beschraenkt.
    #
    # Der String ausserhalb der eckigen Klammern wird durch eine eigene 
    # While-Schleife geprueft. Hierzu werden vorhandene Variablen 
    # zweckentfremded um nicht mehr Variablen deklarieren zu muessen. 
    # Sind die Zeichen in dem nicht eMail-String OK, werden diese 
    # Variablen wieder auf deren Initialwert von -1 gesetzt. 
    #
    # Ist im "nicht eMail-Adress-String" ein ungueltiges Zeichen vorhanden, 
    # wird der Fehler 18 zurueckgegeben. 
    # 

    aktuelles_zeichen = pEingabe[ laenge_eingabe_string - 1 ]
    
    display_string_pos_start = -1
    display_string_pos_end = -1
    
    email_adress_start = 0
    email_adress_end = laenge_eingabe_string - 1

    # 
    # Pruefung: Ende mit einer schliessenden eckigen Klammer ?
    # 
    if ( aktuelles_zeichen == '>' ):

        # 
        # Das letzte Zeichen ist in diesem Fall eine schliessende eckige Klammer.
        # 
        # Dieses Zeichen darf von der unten stehende while-Schleife nicht 
        # geprueft werden, da ansonsten ein ungueltiges Zeichen erkannt 
        # werden wuerde.
        #
        # Es wird die BIS-Poisition fuer die eMail-Adress-Pruefschleife um 
        # ein Zeichen vermindert. 
        # 
        laenge_eingabe_string -= 1

        # 
        # In einer While-Schleife wird die oefnende eckige Klammer gesucht.
        # Es wird von hinten nach vorne gesucht.
        # 
        akt_index = laenge_eingabe_string

        while ( ( akt_index > 0 ) and ( aktuelles_zeichen != '<' ) ):
        
            akt_index -= 1

            aktuelles_zeichen = pEingabe[ akt_index ];

        # 
        # Ist das letzte Zeichen eine schliessende eckige Klammer, muss es eine 
        # eckige startende Klammer geben. 
        # 
        # Nach der While-Schleife muss in der Variablen "aktuelles_zeichen"
        # die oeffnede eckige Klammer enthalten sein. 
        #
        # Ist es ein anderes Zeichen, stimmt die Struktur nicht.
        # 
        if ( aktuelles_zeichen != '<' ):
            return 16 # Struktur: keine oeffnende eckige Klammer gefunden. 

        # 
        # Bestimmung der Positionen, des seperat zu pruefenden "nicht eMail-Adress-Strings"
        # 
        display_string_pos_start = 0
        display_string_pos_end = akt_index

        # 
        # Der aktuelle Index steht nun auf der Position der oeffnenden eckigen Klammer. 
        # Das dortige Zeichen wurde geprueft und ist OK, daher wird der Leseprozess 
        # um ein Zeichen weiter gestellt. (Ausserdem Fehlervermeidung Nr. 22 )
        # 
        akt_index += 1
        
        #if ( akt_index == 0 ):
        #    akt_index = 1

        email_adress_start = akt_index
        email_adress_end = laenge_eingabe_string 



    else:

        # 
        # Eingabe endete nicht auf einer schliessenden eckigen Klammer. 
        # Es wird geprueft, ob die Eingabe mit einer eckigen oeffnenden 
        # Klammer startet. 
        #
        # Es wird das aktuelle Zeichen an der Position 0 gelesen.
        # 
        aktuelles_zeichen = pEingabe[ akt_index ]

        if ( aktuelles_zeichen == '<' ):

            # 
            # Startet die Eingabe mit einer eckigen oeffnenden Klammer, wird
            # in einer While-Schleife die schliessende eckige Klammer gesucht.
            # Es wird von vorne nach hinten gesucht.
            # 
            while ( ( akt_index < ( laenge_eingabe_string - 1 ) ) and ( aktuelles_zeichen != '>' ) ):

                akt_index += 1

                aktuelles_zeichen = pEingabe[ akt_index ]

            # 
            # Ist das erste Zeichen eine oeffnende eckige Klammer, muss es eine 
            # eckige schliessende Klammer geben. 
            #
            # Nach der While-Schleife muss in der Variablen "aktuelles_zeichen"
            # die schliessende eckige Klammer enthalten sein. 
            #
            # Ist es ein anderes Zeichen, stimmt die Struktur nicht.
            # 
            if ( aktuelles_zeichen != '>' ):
                return 17 # Struktur: keine schliessende eckige Klammer gefunden. 

            # 
            # Bestimmung der Positionen, des seperat zu pruefenden "nicht eMail-Adress-Strings"
            #
            # Der zu pruefende String startet nach dem Zeichen hinter der aktuellen Position.
            # Der String endet am Index des letzten Zeichens.
            # 
            display_string_pos_start = akt_index + 1
            display_string_pos_end = laenge_eingabe_string

            email_adress_start = 1
            email_adress_end = akt_index 

            # 
            # Der Leseprozess muss ein Zeichen vor der gefundenden schliessenden eckigen Klammer enden.
            # Die Laenge des Eingabestrings wird entsprechend angepasst.  
            # 
            laenge_eingabe_string = akt_index

            # 
            #Das Zeichen an Position 0 ist die oeffnende eckige Klammer. 
            #Der Leseprozess muss bei Index 1 starten.  
            # 
            akt_index = 1

    email_local_part_gesamt_start = akt_index

    email_local_part_start = akt_index

    # 
    # Pruefung: gibt es einen seperat zu pruefenden "nicht eMail-Adress-String" ?
    # 
    if ( display_string_pos_start != -1 ):
        # 
        # Eingabe = "<ABC@DEF.GHI>"
        #
        # Von der Suchroutine wird eine spitze Klammer erkannt. Es wird auch 
        # eine - in diesem Fall - oeffnende Klammer gefunden. 
        #
        # Es wird die Position des letzten Punktes auf 0 gestellt. 
        # Es bleibt jedoch kein "nicht eMail-String" uebrig. 
        #
        # Ist das ein Fehler oder nicht ?
        # Im Moment wird eine solche Eingabe als korrekte eMail-Adresse durchgelassen. 
        # 
        #if ( position_letzter_punkt == position_kommentar_ende )
        #{
        #  return 19 # Struktur: es gibt keinen "nicht eMail-String" 
        #}

        temp_index = display_string_pos_start      
        
        # 
        # Ueber eine While-Schleife werden die Zeichen im "nicht eMail-Adress-String" geprueft.
        # Wird ein ungueltiges Zeichen erkannt, wir der Fehler 18 zurueckgegeben.
        # 
        while ( temp_index < display_string_pos_end ):
            
            aktuelles_zeichen = pEingabe[ temp_index ]

            if ( ( ( aktuelles_zeichen >= 'a' ) and ( aktuelles_zeichen <= 'z' ) ) or ( ( aktuelles_zeichen >= 'A' ) and ( aktuelles_zeichen <= 'Z' ) ) or ( ( aktuelles_zeichen >= '0' ) and ( aktuelles_zeichen <= '9' ) ) ):
                ()
                # OK
            
            elif ( ( aktuelles_zeichen == ' ' ) or ( aktuelles_zeichen == '(' ) or ( aktuelles_zeichen == ')' ) or ( aktuelles_zeichen == '\"' ) ):
                ()
                # OK ... eventuell weitere Zeichen hier zulaessig, welche zu ergaenzen waeren
            
            elif ( aktuelles_zeichen == '\\' ):

                # 
                # Maskiertes Zeichen 
                # Der Leseprozess muss noch das naechste Zeichen pruefen. 
                # Der Leseprozessindex wird um ein Zeichen weiter gestellt.
                # 
                temp_index += 1

                # 
                # Pruefung: Stringende ?
                # 
                if ( temp_index == display_string_pos_end ):
                    return 83 # String: Escape-Zeichen nicht am Ende der Eingabe

                # 
                # Zeichen nach dem Backslash lesen. 
                # Das Zeichen darf ein Backslash oder ein Anfuehrungszeichen sein. 
                # Alle anderen Zeichen fuehren zum Fehler 84.
                # 
                aktuelles_zeichen = pEingabe[ temp_index ]

                if ( ( aktuelles_zeichen != '\\' ) and ( aktuelles_zeichen != '@' ) and ( aktuelles_zeichen != ' ' ) and ( aktuelles_zeichen != '\'' ) and ( aktuelles_zeichen != '\"' ) ):
                    return 84 # String: Ungueltige Escape-Sequenz im String
                
            else:
                # print( f"Fehler Display String Zeichen {aktuelles_zeichen} " );

                return 18 # Struktur: Fehler: Falsches Zeichen im Display String
            

            temp_index += 1      

            # 
            # Restaurierung der Vorgabewerte
            # Die temporaer fuer andere Zwecke verwendeten Variablen, werden wieder auf deren 
            # Vorgabewerte von -1 gestellt, damit die eigentliche Pruefroutine korrekt arbeitet.
            # 
            position_letzter_punkt = -1
            position_kommentar_ende = -1

    email_local_part_start = 0
    email_domain_part_ende = laenge_eingabe_string - 1

    # 
    # Berechnung der Laenge der reinen eMail-Adressangabe.
    #
    # Die Variable "akt_index" steht hier auf dem ersten Zeichen der eMail-Adresse. 
    # Die Variable "laenge_eingabe_string" steht nach dem letzten zu pruefenden 
    # Zeichen der eMail-Adresse. Dieses um mit der bisherigen Variablenbezeichnung 
    # konform zu sein, welches die Laenge des Eingabestrings war. 
    # 
    zeichen_zaehler =  ( email_adress_end - email_adress_start ) + 1

    #zeichen_zaehler = laenge_eingabe_string - akt_index

    # 
    # http://de.wikipedia.org/wiki/E-Mail-Adresse
    # Innerhalb von RFC 5322 gibt es keine Laengenbegrenzung fuer eMail-Adressen. 
    #
    # Im RFC 5321 wird die maximale Laenge des Local-Parts mit 64 Bytes und
    # die maximale Laenge des Domainnamens mit 255 Bytes angegeben. Zusammen 
    # mit dem "@"-Zeichen ergaebe sich daraus die maximale Laenge einer 
    # E-Mail-Adresse von 320 Bytes. 
    #
    # Im RFC 5321 wird auch die maximale Laenge des "Path"-Elements definiert, 
    # welches die Elemente "FROM" und "RCPT TO" im Envelope bestimmt und die 
    # maximale Laenge von Bytes einschliesslich der Separatoren "<" und ">" hat. 
    # Daraus ergibt sich eine maximale Laenge der E-Mail-Adresse von 254 Bytes 
    # einschliesslich des "@". Eine E-Mail mit einer laengeren Adresse, kann 
    # ueber RFC-konforme SMTP-Server weder verschickt noch empfangen werden.
    #
    # Minimal moegliche eMail-Adresse ist "A@B.CD", gleich 6 Stellen.
    # 
    if ( ( zeichen_zaehler < 6 ) or ( zeichen_zaehler > 254 ) ):
        return 12 # Laenge: Laengenbegrenzungen stimmen nicht 

    zeichen_zaehler = 0

    # 
    # Variable "fkt_ergebnis_email_ok"
    # 
    # Speicherung des Funktionsergebnisses fuer korrekte eMail-Angaben. 
    # 
    # Ist die eMail-Adresse rein Text ohne Sonderformen, bleibt der Wert auf 0.
    # 
    # Ist im Local-Part ein String vorhanden, wird der Wert auf 1 geaendert.
    # 
    # Ist eine IP4-Adressangabe vorhanden, wird der Wert um 2 erhoeht.
    # 
    # Ist eine IP6-Adressangabe vorhanden, wird der Wert um 4 erhoeht.
    # 
    # Ist ein Kommentar vorhanden, wird der Rueckgabewert konvertiert.
    # 
    # Es werden nur die unten stehenden 10 Ergebniswerte geliefert, 
    # damit korrekte eMail-Adressen unter dem Wert 10 bleiben.
    # 
    # Bezueglich der Erhoehung des Wertes bei einer Stringangabe ist es 
    # so, dass die IP-Adresse erst nach dem AT-Zeichen korrekt erkannt
    # wird. Eine korrekt gelesene String-Angabe wird immer vor einer 
    # moeglichen IP-Adresse gelesen werden und somit wird der Ergebnis-
    # wert auf 1 gestellt, bevor die Erhoehung bei der IP-Adresse 
    # gemacht werden kann.   
    # 
    # Folgende Ergebnisse sind moeglich:
    # 
    #  0 = eMail-Adresse korrekt
    #  1 = eMail-Adresse korrekt (Local Part mit String)
    #  2 = eMail-Adresse korrekt (IP4-Adresse)
    #  3 = eMail-Adresse korrekt (Local Part mit String und IP4-Adresse)
    #  4 = eMail-Adresse korrekt (IP6-Adresse)
    #  5 = eMail-Adresse korrekt (Local Part mit String und IP6-Adresse)
    #  6 = eMail-Adresse korrekt (Kommentar)
    #  7 = eMail-Adresse korrekt (Kommentar, String)
    #  8 = eMail-Adresse korrekt (Kommentar, String, IP4-Adresse)
    #  9 = eMail-Adresse korrekt (Kommentar, String, IP6-Adresse)
    #  
    # Durch die verschiedenen Rueckgabewerte, kann der Aufrufer eMail-Adressen 
    # mit IP-Adresse oder String-Teilen im Nachgang noch abweisen.  
    # 
    fkt_ergebnis_email_ok = 0

    knz_kommentar_abschluss_am_stringende = False

    if ( ( laenge_eingabe_string < 6 ) or ( laenge_eingabe_string > 254 ) ):
        return 12 # Laenge: Laengenbegrenzungen stimmen nicht

    email_local_part_gesamt_start = akt_index
    
    email_local_part_start = email_adress_start
    
    #
    # While-Schleife 1
    # 
    # In der aeusseren While-Schleife wird eine grundlegende eMail-Adressstruktur geparst. 
    #
    while ( akt_index < laenge_eingabe_string ):
        
        aktuelles_zeichen = pEingabe[ akt_index ]
        
        #print(f' {akt_index} {aktuelles_zeichen}')

        # 
        # Bedingungen Zeichen A-Z, a-z und Zahlen
        # 
        if ( ( ( aktuelles_zeichen >= 'a' ) and ( aktuelles_zeichen <= 'z' ) ) or ( ( aktuelles_zeichen >= 'A' ) and ( aktuelles_zeichen <= 'Z' ) ) or ( ( aktuelles_zeichen >= '0' ) and ( aktuelles_zeichen <= '9' ) ) ):
            
            # 
            # Buchstaben ("A" bis "Z" und "a" bis "z") und Zahlen duerfen an jeder Stelle der eMail-Adresse vorkommen.
            # 
            # Ein solches Zeichen kann selber keinen Fehler produzieren.
            #
            # Es wird der Zeichenzaehler um eins erhoeht.
            # 
            zeichen_zaehler += 1
            
        elif ( ( aktuelles_zeichen == '_' ) or ( aktuelles_zeichen == '-' ) ):
      
            # 
            # Im Domain-Part duerfen die Sonderzeichen '_' und '-' nicht am Start stehen.  
            # 
            # Steht der Zeichenzaehler auf 0, steht das aktuelle Zeichen an einer ungueltigen Position.
            # 
            # Nach RFC 952 darf im Domain-Part kein Teilstring mit einer Zahl oder einem Punkt starten.
            # Nach RFC 1123 duerfen Hostnamen mit Zahlen starten.
            # 
            # 
            # https://verifalia.com/help/email-validations/can-email-addresses-have-hyphens-minus-signs-dashes
            # 
            # Placement - email addresses cannot have a hyphen (or minus sign, or dash) as the first or last letter in 
            # the domain part. Similarly, the hyphen cannot be placed directly in front of or following, the dot (.). 
            # Have a look at some examples of correct vs. incorrect use:
            # 
            # Correct
            # 
            # username@exam-ple.com
            # username@e-xample.com
            # 
            # Incorrect
            # 
            # username@example-.com
            # username@-example.com
            # 

            if ( akt_index == email_local_part_start ):
            
                if ( pEingabe[ akt_index + 1 ] == '\"' ):
                    return 140 # Trennzeichen: ungueltige Zeichenkombination -"

                if ( pEingabe[ akt_index + 1 ] == '(' ):
                    return 141 # Trennzeichen: ungueltige Zeichenkombination -(

            # 
            # Pruefung: Befindet sich der Leseprozess im Domain-Part ?
            # 
            # Im Domain-Part ist der Leseprozess, wenn die Position des At-Zeichens groesser als 0 ist.
            # 
            if ( position_at_zeichen > 0 ):
        
                if ( zeichen_zaehler == 0 ):
                    return 20 # Zeichen: Zahl oder Sonderzeichen nur nach einem Buchstaben (Teilstring darf nicht mit Zahl oder Sonderzeichen beginnen)

                if ( ( akt_index + 1 ) == laenge_eingabe_string ):
                    return 24 # Zeichen: Kein Sonderzeichen am Ende der eMail-Adresse
                
                else:

                    # 
                    # https://en.wikipedia.org/wiki/Email_address
                    #
                    # Domain-Part:
                    # hyphen -, provided that it is not the first or last character.
                    # 
                    if ( pEingabe[ akt_index + 1 ] == '.' ):
                        return 20 # Trennzeichen: ungueltige Zeichenkombination "-."

        elif ( aktuelles_zeichen == '.' ):

            # 
            # Bedingungen fuer einen Punkt
            # 
      
            # 
            # Pruefung: Wurde schon ein Punkt gefunden?
            # 
            # Nein, wenn in der Speichervariablen "position_letzter_punkt" noch der Initialwert von -1 steht.
            # 
            if ( position_letzter_punkt == -1 ):
            
                # 
                # Pruefung: Leseposition gleich 0 ?
                # 
                # Ist der aktuelle Index gleich 0 und das aktuelle Zeichen ein Punkt,
                # wird der Fehler 30 zurueckgegeben. 
                # 
                # Es darf nicht mit dem Zeichenzaehler geprueft werden, da der erste 
                # Local-Part auch ein String sein kann. Dort wird der Zeichenzaehler 
                # nicht erhoeht.
                # 
                if ( akt_index == ( position_kommentar_ende + 1 ) ):
                    return 30 # Trennzeichen: kein Beginn mit einem Punkt

                # 
                # Der erste Punkt darf nicht am gespeicherten Beginn der eMail-Adresse liegen. 
                # Wichtig bei Eckigen-Klammern, bei welchen die eMail-Adresse nicht am 
                # Index 0 beginnt.
                # 
                if ( akt_index == email_local_part_start ):
                    return 142 # Trennzeichen: kein Beginn mit einem Punkt
            else:
                # 
                # Pruefung: Zwei Punkte hintereinander ?
                # 
                # Ist die Differenz von der aktuellen Leseposition und der letzten 
                # Punkt-Position gleich 1, stehen 2 Punkte hintereinander. Es wird 
                # in diesem Fall der Fehler 31 zurueckgegeben.
                # 
                if ( ( akt_index - position_letzter_punkt ) == 1 ):
                    return 31 # Trennzeichen: keine zwei Punkte hintereinander

            if ( position_at_zeichen > 0 ):
                # 
                # Domain-Part-Labellaenge
                # https://de.wikipedia.org/wiki/Hostname
                # https://en.wikipedia.org/wiki/Hostname
                #    
                # Ein Domain-Label muss 1 Zeichen umfassen und darf maximal 63 Zeichen lang sein. 
                # Bei der Berechnung wird auf 64 Zeichen geprueft, da so die Subtraktion nicht 
                # verkompliziert werden muss (es wird die Position des letzten Punktes mitgezaehlt).
                #    
                # Es muss hier der Index fuer den eigentlichen eMail-Start beruecksichtigt werden. 
                # Normalerweise startet die eMail-Adresse bei Index 0. Bei eMail-Adressen mit 
                # spitzen Klammern kann der Start spaeter sein.
                #    
                # Ist der aktuelle Domain-Label zu lang, wird der Fehler 63 zurueckgegeben.
                # 
                if ( ( akt_index - position_letzter_punkt ) > email_local_part_start + 64 ):
                    return 63 # Domain-Part: Domain-Label zu lang (maximal 63 Zeichen)

            # 
            # Index des letzten Punktes speichern
            # 
            position_letzter_punkt = akt_index

            # 
            # Zeichen- und Zahlenzaehler nach einem Punkt auf 0 stellen
            # 
            zeichen_zaehler = 0

        elif ( aktuelles_zeichen == '@' ):
            # 
            # Bedingungen fuer das AT-Zeichen
            # 

            # 
            # Pruefung: Position AT-Zeichen ungleich -1 ?
            #    
            # Wurde bereits ein AT-Zeichen gefunden, ist in der Positionsvariablen 
            # ein Wert groesser 0 vorhanden. Es darf im Leseprozess nur einmal 
            # ein (unmaskiertes) AT-Zeichen als Trennerzeichen gefunden werden. 
            # Ist schon eine AT-Zeichenposition vorhanden, wird der Fehler
            # 29 zurueckgegeben. 
            #    
            # Wurde noch kein AT-Zeichen gefunden, werden weitere Pruefungen gemacht. 
            # 
            if ( position_at_zeichen != -1 ):
                return 29 # AT-Zeichen: kein weiteres AT-Zeichen zulassen, wenn schon AT-Zeichen gefunden wurde

            if ( akt_index == email_local_part_start ):
                return 26 # AT-Zeichen: kein AT-Zeichen am Anfang

            if ( akt_index > email_local_part_start + 64 ):
                return 13 # Laenge: RFC 5321 = SMTP-Protokoll = maximale Laenge des Local-Parts sind 64 Bytes

            if ( ( akt_index + 1 ) == laenge_eingabe_string ):
                return 27 # AT-Zeichen: kein AT-Zeichen am Ende

            if ( akt_index - position_letzter_punkt == 1 ):
                return 32 # Trennzeichen: ungueltige Zeichenkombination ".@"
        
            # 
            # Kombination "@."
            # An dieser Position ist sichergestellt, dass in der Eingabe noch 
            # mindestens 1 Zeichen folgt. Es gibt hier keine Index-Out-Of-Bounds Exception.
            #  
            # Ansonsten wuerde das AT-Zeichen am Ende stehen und der Aufrufer 
            # wuerde 8 als Funktionsergebnis bekommen.
            # 
            if ( pEingabe[ akt_index + 1 ] == '.' ):
                return 33 # Trennzeichen: ungueltige Zeichenkombination "@."

            # 
            # Position des AT-Zeichens merken
            # 
            position_at_zeichen = akt_index

            # 
            # Zeichenzaehler nach dem AT-Zeichen auf 0 stellen
            # 
            zeichen_zaehler = 0

            # 
            # Position letzer Punkt
            #    
            # Das AT-Zeichen trennt den Local- und Domain-Part. 
            # Die Position des letzen Punkts muss ausgenullt werden, um 
            # Seiteneffekte bei der Laengenberechnung der einzelnen 
            # Domain-Parts zu vermeiden.
            #    
            # Der Domain-Part startet am AT-Zeichen und auf dessen Index 
            # wird auch die Position des letzten Punktes gesetzt.
            # 
            position_letzter_punkt = akt_index
            
            # 
            # ------------------------------- IP 4 ohne eckige Klammern ---------------------------------------
            #    
            # Nach dem AT-Zeichen kann eine IP4-Adresse ohne eckige Klammern stehen.
            # Wie z.B. folgende eMail-Adresse:
            #    
            #     ip4.without.brackets@127.0.0.1
            #             
            # Ist das auf das AT-Zeichen folgende Zeichen eine Zahl, wird in einer 
            # While-Schleife versucht, eine gueltige IP4 Adresse zu lesen.  
            #    
            # Es handelt sich um eine IP4-Adresse, wenn die nachfolgenden Zeichen 
            # nur Ziffern und 3 Punkte sind. 
            #    
            # Ist eine IP4-Adresse erkannt worden, muss die Angabe nicht korrekt sein:
            #     
            #     byte.overflow@127.0.999.1
            #     zu.viele.ziffern@127.0.0001.1
            #     zu.viele.ziffern@127.0.1234.1
            #     keine.zahl.zwischen.punkten@127...1
            #     
            # Alle anderen Eingaben werden nicht als IP4-Angabe gewertet und werden 
            # durch die aeussere While-Schleife abgearbeitet. Das koennen folgende 
            # eMail-Adressen sein:
            #    
            #     negative.zahl@127.0.-1.1
            #     zu.viele.punkte@127.0..0.1
            #     keinen.punkt.im.domain.part@127001
            #     punkt.am.ende@127.0.0.
            #     tld.zu.kurz@127.0.A.1
            #     zu.viele.angaben@127.0.0.1.127.0.0.1
            #    
            # 

            next_char = pEingabe[ akt_index + 1 ]

            if ( ( next_char >= '0' ) and ( next_char <= '9' ) ):

                knz_ist_ip4_adresse = 0

                next_pos = akt_index + 1

                # 
                # Innere While-Schleife
                # In einer inneren While-Schleife wird die IP-Adresse geparst und 
                # auf Gueltigkeit geprueft. 
                #    
                # Die innere While-Schleife laeuft bis zum Ende des Eingabestrings.
                # 
                ip_adresse_akt_zahl = 0

                ip_adresse_zahlen_zaehler = 0

                ip_adresse_zaehler_trennzeichen = 0

                ip_adresse_pos_letzter_punkt = 0

                while ( ( next_pos < laenge_eingabe_string ) and ( next_pos != -1 ) ):

                    # 
                    # Aktuelles Pruefzeichen
                    # Das aktuelle Zeichen wird aus der Eingabe am aktuellen Index herausgelesen. 
                    # 
                    next_char = pEingabe[ next_pos ]

                    # 
                    # Die IP-Adresse besteht nur aus Zahlen und Punkten mit einem 
                    # abschliessendem "]"-Zeichen. Alle anderen Zeichen fuehren 
                    # zu dem Fehler 59 = ungueltiges Zeichen.
                    #    
                    # Es wird nur eine IP4 Adresse geprueft.
                    # 
                    if ( ( next_char >= '0' ) and ( next_char <= '9' ) ):
            
                        # 
                        # Zahlen
                        # - nicht mehr als 3 Ziffern
                        # - nicht groesser als 255 (= 1 Byte)
                        # 

                        # 
                        # Zahlenzaehler
                        # Der Zahlenzaehler wird erhoeht.
                        # Anschliessend wird geprueft, ob schon mehr als 3 Zahlen gelsen wurden. 
                        # Ist das der Fall, wird 53 zurueckgegeben. 
                        # 
                        ip_adresse_zahlen_zaehler += 1

                        if ( ip_adresse_zahlen_zaehler > 3 ):

                            knz_ist_ip4_adresse = 53 # IP4-Adressteil: zu viele Ziffern, maximal 3 Ziffern
                        
                        else:
                        
                            # 
                            # Berechnung Akt-Zahl
                            # Der Wert in der Variablen "akt_zahl" wird mit 10 multipliziert und 
                            # der Wert des aktullen Zeichens hinzugezaehlt. 
                            #    
                            # Der Wert des aktuellen Zeichens ist der Wert des ASCII-Code abzueglich 48.
                            #    
                            # Anschliessend wird geprueft, ob die Zahl groesser als 255 ist. 
                            # Ist die Zahl groesser, wird 54 zurueckgegeben. (Byteoverflow)
                            # 
                            ip_adresse_akt_zahl = ( ip_adresse_akt_zahl * 10 ) + ( ( (int( ord(next_char)) ) ) - 48 )
                            
                            if ( ip_adresse_akt_zahl > 255 ):
                                knz_ist_ip4_adresse = 54 # IP4-Adressteil: Byte-Overflow

                    elif ( next_char == '.' ):
                        
                        # 
                        # Punkt (Trennzeichen Zahlen)
                        # 

                        # 
                        # Pruefung: Zahlen vorhanden ?
                        #    
                        # Steht der Zahlenzaehler auf 0, wurden keine Zahlen gelesen. 
                        # In diesem Fall wird 55 zurueckgegeben.
                        # 
                        if ( ip_adresse_zahlen_zaehler == 0 ):
                            knz_ist_ip4_adresse = 55 # IP4-Adressteil: keine Ziffern vorhanden

                        # 
                        # ANMERKUNG FEHLER 63 
                        # Dieser Fehlercode kann nicht kommen, da bei 2 hintereinanderkommenden 
                        # Punkten keine Zahl gelesen worden sein kann. Dieses ist die  
                        # vorhergehende Pruefung.
                        #    
                        # Es kann auch kein anderes Zeichen gelesen worden sein, das 
                        # wuerde einen anderen Fehler verursachen.
                        # 
                        # 
                        # 
                        # Pruefung: 2 Punkte hintereinander ?
                        # Die letzte Position eines Punktes, darf nicht vor der aktuellen 
                        # Lesepostion liegen. Ist das der Fall, wird 63 zurueckgegeben.
                        # 
                        # if ( ( akt_index - ip_adresse_pos_letzter_punkt ) == 1 )
                        # {
                        #   return 63; # IP4-Adressteil: keine 2 Punkte hintereinander
                        # }

                        # 
                        # Anzahl Trennzeichen
                        # Es duerfen nicht mehr als 3 Punkte (=Trennzeichen) gelesen werden. 
                        # Beim 4ten Punkt, wird 56 zurueckgegeben.
                        # 
                        ip_adresse_zaehler_trennzeichen += 1

                        if ( ip_adresse_zaehler_trennzeichen > 3 ):
                            knz_ist_ip4_adresse = 56 # IP4-Adressteil: zu viele Trennzeichen

                        # 
                        # Sind alle Pruefungen fuer einen Punkt durchgefuehrt worden, 
                        # wird die Position des letzten Punktes aktualisiert. 
                        #    
                        # Es wird der Zahlenzaehler und der Wert der aktuellen Zahl auf 0 gestellt.
                        # 
                        ip_adresse_pos_letzter_punkt = next_pos

                        ip_adresse_zahlen_zaehler = 0

                        ip_adresse_akt_zahl = 0
                    
                    else:
                        
                        # 
                        # Ungueltiges Zeichen
                        # Bei einem ungueltigem Zeichen wird die Variable "next_pos" auf 
                        # -2 gestellt. Nach dem darauffolgendem increment, wird die 
                        # Variable dann den Wert -1 haben, welches eine Bedingung fuer
                        # das Schleifen ende ist.
                        # 
                        next_pos = -2

                    next_pos += 1

                if ( next_pos == -1 ):
                    ()
                    # 
                    # Es wurde keine gueltige IP4 Adresse gelesen. 
                    # Die aeussere While-Schleife prueft die eMail-Adresse weiter
                    # 
                
                elif ( next_pos == laenge_eingabe_string ):
          
                    # 
                    # Fuer eine gueltige IP4-Adresse muss der Leseprozess sich am Ende der 
                    # Eingabe befinden.
                    # 

                    # 
                    # Anzahl Trennzeichen
                    # Fuer eine IP4-Adresse muessen 3 Punkte gelesen worden sein. 
                    # 
                    if ( ip_adresse_zaehler_trennzeichen == 3 ):
                    
                        # 
                        # Der letzte Punkt darf nicht auf der vorhergehenden Punkt-Position liegen. 
                        # 
                        if ( ( next_pos - ip_adresse_pos_letzter_punkt ) != 1 ):

                            if ( knz_ist_ip4_adresse != 0 ):
                            
                                # 
                                # Wurde ein Fehler in der While-Schleife festgestellt, 
                                # wird dieser dem Aufrufer zurueckgegeben.
                                #    
                                # Es handelt sich hierbei um eine IP4-Adresse, welche falsch ist.
                                # Byte-Overflow, zwischen 2 Punkten keine Zahl, zu viele Ziffern.
                                # 
                                return knz_ist_ip4_adresse
                            
                            else:

                                # 
                                # Ist die IP4-Adresse korrekt, werden die Variablen der aeusseren 
                                # While-Schleife auf die gueltigen Werte gesetzt.
                                # 
                                position_letzter_punkt = ip_adresse_pos_letzter_punkt

                                akt_index = next_pos - 1 # Eine Stelle zu weit gelesen

                                fkt_ergebnis_email_ok = 2 # Ergebnis ist eine eMail mit einer IP4-Adresse

                            # 
                            # Eine Pruefung auf den Zahlenzaehler bringt nichts. 
                            # Der Zahlenzaehler ist im eventuellen Fehlerfall hier 0. 
                            # Wuerde eine Zahl gelesen, wuerde ein Fehler bei den  
                            # Zahlen geprueft werden.
                            #    
                            # Wuerde versucht werden, den Punkt und das Abschlusszeichen 
                            # mit anderen Zeichen zu trennen, wuerde ein ungueltiges 
                            # Zeichen erkannt werden. 
                            # 

            # 
            # ------------------------------- IP 4 ohne eckige Klammern ---------------------------------------
            #             
            
        elif ( aktuelles_zeichen == '\\' ):
            # 
            # Sonderzeichen mit Qoutierung, welche nur im Local-Part vorkommen duerfen
            #  
            # \ @
            #  
            # Ist die Positon fuer das AT-Zeichen groesser als 0, befindet sich 
            # der Leseprozess im Domain-Part der eMail-Adresse. Dort sind diese 
            # Zeichen nicht erlaubt und es wird 21 zurueckgegeben.
            # 
            if ( position_at_zeichen > 0 ):
                return 21 # Zeichen: Sonderzeichen im Domain-Part nicht erlaubt

            # 
            # Maskiertes Zeichen 
            # Der Leseprozess muss noch das naechste Zeichen pruefen. 
            # Der Leseprozessindex wird um ein Zeichen weiter gestellt.
            # 
            akt_index += 1

            # 
            # Pruefung: Stringende ?
            # 
            if ( akt_index == laenge_eingabe_string ):
                return 83 # String: Escape-Zeichen nicht am Ende der Eingabe

            # 
            # Zeichen nach dem Backslash lesen. 
            # Das Zeichen darf ein Backslash oder ein Anfuehrungszeichen sein. 
            # Alle anderen Zeichen fuehren zum Fehler 84.
            # 
            aktuelles_zeichen = pEingabe[ akt_index ]

            if ( ( aktuelles_zeichen != '\\' ) and ( aktuelles_zeichen != '@' ) and ( aktuelles_zeichen != ' ' ) and ( aktuelles_zeichen != '\'' ) ):
                return 84 # String: Ungueltige Escape-Sequenz im String
            
            aktuelles_zeichen = 'A'
        
        elif ( ( aktuelles_zeichen == '!' ) or ( aktuelles_zeichen == '#' ) or ( aktuelles_zeichen == '$' ) or ( aktuelles_zeichen == '%' ) or ( aktuelles_zeichen == '&' ) or ( aktuelles_zeichen == '\'' ) or ( aktuelles_zeichen == '*' ) or ( aktuelles_zeichen == '+' ) or ( aktuelles_zeichen == '-' ) or ( aktuelles_zeichen == '/' ) or ( aktuelles_zeichen == '=' ) or ( aktuelles_zeichen == '?' ) or ( aktuelles_zeichen == '^' ) or ( aktuelles_zeichen == '`' ) or ( aktuelles_zeichen == '{' ) or ( aktuelles_zeichen == '|' ) or ( aktuelles_zeichen == '}' ) or ( aktuelles_zeichen == '~' ) ):
            # 
            #    asc("!") = 033   asc("*") = 042 
            #    asc("#") = 035   asc("+") = 043 
            #    asc("$") = 036   asc("-") = 045 
            #    asc("%") = 037   asc("/") = 047
            #    asc("&") = 038 
            #    asc("'") = 039
            #    
            #    asc("=") = 061   asc("{") = 123 
            #    asc("?") = 063   asc("|") = 124 
            #    asc("^") = 094   asc("}") = 125 
            #    asc("_") = 095   asc("~") = 126 
            #    asc("`") = 096   asc(" ") = 032 
            # 
            #    
            # 
            # Sonderzeichen, welche nur im Local-Part vorkommen duerfen
            #  
            # !#$%&'*+-/=?^_`{|}~
            #  
            # Ist die Positon fuer das AT-Zeichen groesser als 0, befindet sich 
            # der Leseprozess im Domain-Part der eMail-Adresse. Dort sind diese 
            # Zeichen nicht erlaubt und es wird 21 zurueckgegeben.
            # 
            if ( position_at_zeichen > 0 ):
                return 21 # Zeichen: Sonderzeichen im Domain-Part nicht erlaubt

        elif ( aktuelles_zeichen == '"' ):
        
            # 
            # While-Schleife 2 - String
            # 
            #    
            # 
            # Pruefung: Leseprozess im Domain-Part ?
            # Im Domain-Part sind keine Anfuehrungszeichen erlaubt. 
            # Es wird der Fehler 82 zurueckgegeben.
            # 
            if ( position_at_zeichen > 0 ):
                return 82 # String: kein Anfuehrungszeichen nach dem AT-Zeichen

            # 
            # Pruefung: Zeichenkombination ."
            #    
            # Ein lokaler Part in Anfuehrungszeichen muss nach einem Trennzeichen starten.
            #    
            # Wurde schon ein Punkt gefunden und die Differenz des Leseprozesses 
            # ist nicht 1, wird der Fehler 81 zurueckgegeben.
            # 
            if ( position_letzter_punkt > 0 ):
                if ( akt_index - position_letzter_punkt != 1 ):
                    return 81 # String: Ein startendes Anfuehrungezeichen muss direkt nach einem Punkt kommen

            # 
            # Pruefung: Start mit Anfuehrungszeichen 
            # Ein Anfuehrungszeichen darf nur am Beginn eines Blockes kommen. 
            # Wurden im aktuellem Block schon zeichen gelesen, ist ein startendes Anfuehrungszeichen
            # falsch gesetzt. Es wird der Fehler 80 zurueckgegeben.
            #    
            # anders:
            #    
            # Der Zeichenzaehler muss fuer den aktuellen Block 0 sein. Der Zeichenzaeler ist 
            # fuer den aktuellen Block 0 am Start oder nach einem Punkt.
            #    
            # 
            if ( zeichen_zaehler > 0 ):
                return 80 # String: Ein startendes Anfuehrungszeichen muss am Anfang kommen, der Zeichenzaehler darf nicht groesser als 0 sein

            # 
            # Das aktuelle Zeichen ist hier noch ein Anfuehrungszeichen. 
            # Die nachfolgende While-Schleife wuerde nicht starten, wenn 
            # das Zeichen nicht geaendert wuerde. Darum wird der Variablen 
            # "aktuelles_zeichen" das Zeichen 'A' zugewiesen.
            # 
            aktuelles_zeichen = 'A'

            # 
            # Position des aktuellen Anfuehrungszeichens merken
            # 
            position_anf_zeichen_akt = akt_index

            # 
            # Der Leseprozess wird um ein Zeichen weitergestellt. 
            # Damit wird das einleitende Anfuehrungszeichen vom Parser verarbeitet.
            #    
            # Steht das einleitende Anfuehrungszeichen am Stringende, wird die 
            # While-Schleife nicht ausgefuehrt, da die Variable "akt_index" jetzt 
            # gleich der Laenge des Eingabestrings ist. Die Differenz zur 
            # gespeicherten Position des einleitenden Anfuehrungszeichens ist 1. 
            # Das ist die erste Pruefung nach der While-Schleife. Es werden 
            # somit Eingaben wie:
            #    
            #         ABC.DEF."
            #    
            # erkannt. Der Aufrufer bekommt in diesem Fall den Fehler 85 zurueck.
            # 
            akt_index += 1

            # 
            # Innere While-Schleife zum Einlesen des Strings.
            # Laeuft bis zum Stringende oder bis zum naechsten - nicht maskierten - Anfuehrungszeichen.
            # 
            while ( ( akt_index < laenge_eingabe_string ) and ( aktuelles_zeichen != '"' ) ):
            
                # 
                # Aktuelles Pruefzeichen
                # Das aktuelle Zeichen wird aus der Eingabe am aktuellen Index herausgelesen. 
                # 
                aktuelles_zeichen = pEingabe[ akt_index ];

                # 
                # Alle erlaubten Stringzeichen werden durchgelassen. 
                # Falsche Zeichen erzeugen einen Fehler.
                # 

                if ( ( ( aktuelles_zeichen >= 'a' ) and ( aktuelles_zeichen <= 'z' ) ) or ( ( aktuelles_zeichen >= 'A' ) and ( aktuelles_zeichen <= 'Z' ) ) ):
                    ()
                    # OK - Buchstaben
                
                elif ( ( aktuelles_zeichen >= '0' ) and ( aktuelles_zeichen <= '9' ) ):
                    ()
                    # OK - Zahlen
                
                elif ( ( aktuelles_zeichen == '_' ) or ( aktuelles_zeichen == '-' ) or ( aktuelles_zeichen == '@' ) or ( aktuelles_zeichen == '.' ) or ( aktuelles_zeichen == ' ' ) or ( aktuelles_zeichen == '!' ) or ( aktuelles_zeichen == '#' ) or ( aktuelles_zeichen == '$' ) or ( aktuelles_zeichen == '%' ) or ( aktuelles_zeichen == '&' ) or ( aktuelles_zeichen == '\'' ) or ( aktuelles_zeichen == '*' ) or ( aktuelles_zeichen == '+' ) or ( aktuelles_zeichen == '-' ) or ( aktuelles_zeichen == '/' ) or ( aktuelles_zeichen == '=' ) or ( aktuelles_zeichen == '?' ) or ( aktuelles_zeichen == '^' ) or ( aktuelles_zeichen == '`' ) or ( aktuelles_zeichen == '{' ) or ( aktuelles_zeichen == '|' ) or ( aktuelles_zeichen == '}' ) or ( aktuelles_zeichen == '~' ) ):
                    ()
                    # OK - Sonderzeichen 1
                
                elif ( ( aktuelles_zeichen == '(' ) or ( aktuelles_zeichen == ')' ) or ( aktuelles_zeichen == ',' ) or ( aktuelles_zeichen == ':' ) or ( aktuelles_zeichen == ';' ) or ( aktuelles_zeichen == '<' ) or ( aktuelles_zeichen == '>' ) or ( aktuelles_zeichen == '@' ) or ( aktuelles_zeichen == '[' ) or ( aktuelles_zeichen == ']' ) ):
                    ()
                    # OK - Sonderzeichen 2 = (),:;<>@[\]
                
                elif ( aktuelles_zeichen == '"' ):

                    # OK - abschliessendes Anfuehrungszeichen 

                    # 
                    # Der Leseprozessindex muss nach der While-Schleife auf dem jetzt
                    # gerade gueltigen Index stehen. 
                    #    
                    # Da am Ende dieser inneren While-Schleife der Leseprozess um 
                    # eine Position weiter gestellt wird, muss der Index hier um 
                    # eine Position verringert werden.
                    #    
                    # Die aeussere While-Schleife erhoeht den Leseprozessindex nochmals. 
                    # 
                    akt_index -= 1
            
                elif ( aktuelles_zeichen == '\\' ):
                    # 
                    # Maskiertes Zeichen 
                    # Der Leseprozess muss nach naechste Zeichen pruefen. 
                    # Der Leseprozessindex wird um ein Zeichen weiter gestellt.
                    # 
                    akt_index += 1

                    # 
                    # Pruefung: Stringende ?
                    # 
                    if ( akt_index == laenge_eingabe_string ):
                        return 83 # String: Escape-Zeichen nicht am Ende der Eingabe

                    # 
                    # Zeichen nach dem Backslash lesen. 
                    # Das Zeichen darf ein Backslash oder ein Anfuehrungszeichen sein. 
                    # Alle anderen Zeichen fuehren zum Fehler 84.
                    # 
                    aktuelles_zeichen = pEingabe[ akt_index ];

                    if ( ( aktuelles_zeichen != '\\' ) and ( aktuelles_zeichen != '@' ) and ( aktuelles_zeichen != ' ' ) and ( aktuelles_zeichen != '\'' ) and ( aktuelles_zeichen != '"' ) ):
                        return 84 # String: Ungueltige Escape-Sequenz im String

                    # 
                    # Vermeidung dass die While-Schleife fruehzeitig beendet wird. 
                    # Im Falle dass ein Anfuehrungszeichen gefunden wurde, wuerde 
                    # die While-Schleife zum String einlesen beendet werden. 
                    # 
                    aktuelles_zeichen = 'A'
          
                else:
                    
                    # 
                    # Fehler 89
                    # Dieser Fehler wird zurueckgegeben, wenn ein ungueltiges 
                    # Zeichen im String vorhanden ist.
                    # 
                    return 89 # String: Ungueltiges Zeichen innerhalb Anfuehrungszeichen

                # 
                # Der Leseprozessindex wird um eine Position weitergestellt.
                # 
                akt_index += 1

            # 
            # Leerstring 
            # Wird ein abschliessendes Leerzeichen gefunden, darf die Differenz zur
            # letzten Position eines Anfuehrungszeichens nicht 1 sein.
            # 
            if ( ( akt_index - position_anf_zeichen_akt ) == 1 ):
                return 85 # String: Leerstring in Anfuehrungszeichen "", oder Start mit Leerzeichen am Ende der Eingabe

            # 
            # Pruefung: abschliessendes Anfuehrungszeichen vorhanden ?
            #    
            # Nach dem Ende der While-Schleife, muss die Variable "aktuelles_zeichen" ein 
            # Anfuehrungszeichen beinhalten. 
            #    
            # Wurde kein abschliessendes Anfuehrungszeichen gefunden? 
            # 
            if ( aktuelles_zeichen != '"' ):
                return 86 # String: kein abschliessendes Anfuehrungszeichen gefunden.

            # 
            # Pruefung: Leseprozess am Stringende angelangt ? 
            # 
            if ( akt_index + 1 >= laenge_eingabe_string ):
                return 88 # String: Der String endet am Stringende (Vorzeitiges Ende der Eingabe)

            # 
            # Gueltige Abschlusszeichenkombinationen pruefen
            # 
            if ( pEingabe[ akt_index + 1 ] == '.' ):
                ()
                # gueltige Zeichenkombination ".
            
            elif ( pEingabe[ akt_index + 1 ] == '@' ):
                ()
                # gueltige Zeichenkombination "@
            
            elif ( pEingabe[ akt_index + 1 ] == '(' ):
                ()
                # gueltige Zeichenkombination "(
                    
            else:
                return 87 # String: Nach einem abschliessendem Anfuehrungszeichen muss ein AT-Zeichen oder ein Punkt folgen

            # 
            # Position des letzten Anfuehrungszeichens merken
            # 
            position_anf_zeichen_akt = akt_index

            # 
            # Es wurde ein String im Local-Part der eMail-Adresse erkannt. 
            # Die Variable "fkt_ergebnis_email_ok" wird auf 1 gesetzt.
            # 
            fkt_ergebnis_email_ok = 1
            
        elif ( aktuelles_zeichen == '[' ):
            
            # 
            # While-Schleife 3 - IP-Adresse
            # 
            #    
            # 
            # Pruefung: AT-Zeichen noch nicht vorgekommen ?
            #    
            # Die IP-Adresse muss sich im Domain-Teil der eMail-Adresse befinden. 
            # Wurde noch kein AT-Zeichen gefunden, befindet sich der Leseprozess 
            # noch nicht im Domain-Teil. Es wird 51 als Fehler zurueckgegeben. 
            # 
            if ( position_at_zeichen == -1 ):
                return 51 # IP-Adressteil: IP-Adresse vor AT-Zeichen

            if ( ( position_kommentar_ende > position_at_zeichen ) ):
                # 
                # Pruefung: Domain-Part mit Kommentar nach AT-Zeichen
                #    
                # ABC.DEF@(comment)[1.2.3.4]
                #    
                # Ist ein Kommentar direkt nach dem AT-Zeichen vorhanden, muss die einleitende
                # eckige Klammer fuer die IP-Adresse direkt nach der schliessenden Kommentarklammer
                # kommen. 
                #    
                # Der Abstand der aktuellen Lesepositon zur Position der Kommentarklammer muss 1 betragen. 
                # Ist die Differenz groesser, wird der Fehler 106 zurueckgegeben.
                # 
                if ( ( akt_index - position_kommentar_ende ) != 1 ):
                    return 106 # Kommentar: Domain-Part mit Kommentar nach AT-Zeichen. Erwartete Zeichenkombination ")[".
        
            else:
        
                # 
                # Pruefung: Startzeichen direkt nach AT-Zeichen ?
                #    
                # Das Startzeichen "[" muss direkt nach dem AT-Zeichen kommen. 
                # Die aktuelle Leseposition muss genau 1 Zeichen nach der Position  
                # des AT-Zeichens liegen. Ist das nicht der Fall, wird 
                # 52 als Fehler zurueckgegeben.
                # 
                if ( ( akt_index - position_at_zeichen ) != 1 ):
                    return 52 # IP-Adressteil: IP-Adresse muss direkt nach dem AT-Zeichen kommen (korrekte Kombination "@[")

            # 
            # Kennzeichenfeld IPv6
            #    
            # Ist keine IPv6-Adresse vorhanden, ist der Wert 0.
            #    
            # Ist eine normale IPv6-Adresse vorhanden, ist der Wert 1.
            #    
            # Ist eine IPv6-Adresse mit einer IPv4-Adressangabe vorhanden, ist der Wert 2.
            # 
            knz_ipv6 = 0

            ip_adresse_zaehler_trennzeichen = 0

            ip_adresse_anzahl_trennzeichen_hintereinander = 0

            # 
            # Pruefung: IP-V6 Adressangabe ?
            #    
            # Es wird auf vorhandensein des Strings "IPv6:" ab der aktuellen Leseposition geprueft.
            #    
            # Ist der String vorhanden, wird eine IP-V6 Adresse gelesen. 
            # Ist der String nicht vorhanden, wird eine IP-4 Adresse gelesen.
            #    
            # Die Pruefung wird nur gemacht, wenn ab der aktuellen Position noch mindestens 5 Stellen vorhanden sind.
            #    
            #         1234567890
            #     ABC@[IPv6:1:2::3]
            #     ABC@[123.456.789.012]
            # 
            if ( akt_index + 5 < laenge_eingabe_string ):
        
                # 
                # Ist das naechste Zeichen ein "I", werden die darauffolgenden Zeichen auf 
                # die Zeichen "P", "v", "6" und ":" geprueft. 
                #    
                # Sind diese Zeichen vorhanden, wird eine IPv6-Adresse gelesen.
                #    
                # Sind diese Zeichen nicht vorhanden, ist es ein Fehler, da das einleitende Zeichen "I" falsch ist.
                # In diesem Fall wird der Fehler 40 zurueckgegeben.
                # 
                if ( pEingabe[ akt_index + 1 ] == 'I' ):
          
                    if ( ( pEingabe[ akt_index + 2 ] == 'P' ) and ( pEingabe[ akt_index + 3 ] == 'v' ) and ( pEingabe[ akt_index + 4 ] == '6' ) and ( pEingabe[ akt_index + 5 ] == ':' ) ):
            
                        # 
                        # Der Index des Leseprozesses wird um 5 erhoeht. 
                        # Am schleifenende wird der Prozess nochmals um eine Position weitergestellt.
                        #    
                        # 01234567890123456789
                        # ABC@[IPv6::ffff:127.0.0.1]"
                        # 
                        akt_index += 5

                        # 
                        # Der Leseprozess befindet sich in einer IPv6 Adresse.
                        # Die Kennzeichenvariable wird auf 1 gestellt.
                        # 
                        knz_ipv6 = 1

                        # 
                        # Es wurde 1 Trennzeichen gelesen.
                        # (Trennzeichen zaehlt?)
                        # 
                        ip_adresse_zaehler_trennzeichen += 1
            
                    else:
        
                        return 40 # IP6-Adressteil: String "IPv6:" erwartet
          
                elif ( ( pEingabe[ akt_index + 1 ] == ':' ) or ( pEingabe[ akt_index + 2 ] == ':' ) or ( pEingabe[ akt_index + 3 ] == ':' ) or ( pEingabe[ akt_index + 4 ] == ':' ) or ( pEingabe[ akt_index + 5 ] == ':' ) ):
            
                    # 
                    # Einbettung IP-V6-Adresse ohne Praefix "IPv6"
                    #    
                    # Wird der Praefix "IPv6" nicht gefunden, wird auf das vorhandensein 
                    # eines Doppelpunktes innerhalb der naechsten 5 Zeichen geprueft.
                    # Wird ein Doppelpunkt gefunden, ist dieses das Kennzeichen, dass 
                    # eine IP-V6 Adresse vorhanden ist. 
                    #    
                    # Das erste Zeichen wird auch mit geprueft, da die IP-V6-Adresse mit "::" starten koennte.
                    # 

                    # 
                    # Der Leseprozess befindet sich in einer IPv6 Adresse.
                    # Die Kennzeichenvariable wird auf 1 gestellt.
                    # 
                    knz_ipv6 = 1

            # 
            # https://de.wikipedia.org/wiki/IPv6#Adressaufbau_von_IPv6
            #    
            # Die textuelle Notation von IPv6-Adressen ist in Abschnitt 2.2 von RFC 4291 beschrieben:
            #    
            # IPv6-Adressen werden fuer gewoehnlich hexadezimal (IPv4: dezimal) notiert, 
            # wobei die Zahl in acht Bloecke zu jeweils 16 Bit (4 Hexadezimalstellen) unterteilt wird.
            #    
            # Diese Bloecke werden durch Doppelpunkte (IPv4: Punkte) getrennt 
            # notiert: 2001:0db8:85a3:08d3:1319:8a2e:0370:7344.
            #    
            # Fuehrende Nullen innerhalb eines Blockes duerfen ausgelassen werden: 
            # 2001:0db8:0000:08d3:0000:8a2e:0070:7344 ist gleichbedeutend mit 2001:db8:0:8d3:0:8a2e:70:7344.
            #    
            # Ein oder mehrere aufeinander folgende Bloecke, deren Wert 0 (bzw. 0000) betraegt, duerfen ausgelassen werden. 
            # Dies wird durch zwei aufeinander folgende Doppelpunkte angezeigt: 2001:0db8:0:0:0:0:1428:57ab ist gleichbedeutend mit 2001:db8::1428:57ab.[15]
            #    
            # Die Reduktion durch Regel 3 darf nur einmal durchgefuehrt werden.
            #    
            # Es darf hoechstens eine zusammenhaengende Gruppe aus Null-Bloecken in der Adresse ersetzt werden.
            #    
            # Die Adresse 2001:0db8:0:0:8d3:0:0:0 darf demnach entweder zu 2001:db8:0:0:8d3:: oder 2001:db8::8d3:0:0:0 gekuerzt werden.
            # 2001:db8::8d3:: ist unzulaessig, da dies mehrdeutig ist und faelschlicherweise z.B. auch als 2001:db8:0:0:0:8d3:0:0 interpretiert werden koennte.
            #    
            # Die Reduktion darf auch dann nicht mehrfach durchgefuehrt werden, wenn das Ergebnis eindeutig waere. 
            #    
            # Ebenfalls darf fuer die letzten beiden Bloecke (vier Bytes, also 32 Bits) der Adresse die herkoemmliche dezimale Notation mit Punkten als Trennzeichen verwendet werden. 
            # So ist ::ffff:127.0.0.1 eine alternative Schreibweise fuer ::ffff:7f00:1. Diese Schreibweise wird vor allem bei Einbettung des IPv4-Adressraums in den IPv6-Adressraum verwendet.
            # 
 
            # 
            # Innere While-Schleife
            # In einer inneren While-Schleife wird die IP-Adresse geparst und 
            # auf Gueltigkeit geprueft. 
            #    
            # Die innere While-Schleife laeuft bis zum Ende des Eingabestrings.
            # 

            ip_adresse_akt_zahl = 0

            ip_adresse_zahlen_zaehler = 0

            akt_index += 1

            while ( ( akt_index < laenge_eingabe_string ) and ( aktuelles_zeichen != ']' ) ):
        
                # 
                # Aktuelles Pruefzeichen
                # Das aktuelle Zeichen wird aus der Eingabe am aktuellen Index herausgelesen. 
                # 
                aktuelles_zeichen = pEingabe[ akt_index ];

                if ( knz_ipv6 == 1 ):

                    if ( ( ( aktuelles_zeichen >= 'a' ) and ( aktuelles_zeichen <= 'f' ) ) or ( ( aktuelles_zeichen >= 'A' ) and ( aktuelles_zeichen <= 'F' ) ) or ( ( aktuelles_zeichen >= '0' ) and ( aktuelles_zeichen <= '9' ) ) ):
                    
                        # 
                        # Zahlenzaehler
                        # Der Zahlenzaehler wird erhoeht.
                        # Anschliessend wird geprueft, ob schon mehr als 4 Zeichen gelsen wurden. 
                        # Ist das der Fall, wird 46 zurueckgegeben. 
                        # 
                        ip_adresse_zahlen_zaehler += 1

                        if ( ip_adresse_zahlen_zaehler > 4 ):
                            return 46 # IP6-Adressteil: zu viele Zeichen, maximal 4 Zeichen
                        
                    elif ( aktuelles_zeichen == '.' ):
            
                        # 
                        # IPv4 Adressangabe
                        # Wird innerhalb der IPv6-Adresse eine IPv4-Adresse angegeben, wird 
                        # dieses durch einen Punkt erkannt.  
                        #    
                        # Der Leseprozess wird in die Erkennungsroutine fuer die IPv4-Adresse umgelenkt.
                        #    
                        # Die erste Zahl der IPv4-Adresse muss nochmal gelesen werden, damit die 
                        # IPv4-Erkennungsroutine korrekt pruefen kann. Dazu wird der Leseprozessindex 
                        # auf die Position des letzten Trennzeichens zurueckgesetzt.
                        #    
                        # Die erste Angabe der IPv4-Adresse wird doppelt gelesen. 
                        # 
                        #    
                        # 
                        # Ist eine IP4-Adresse eingebettet worden, muessen Trennzeichen 
                        # der IPv6-Adresse gefunden worden sein.  
                        #    
                        # (Nach dem aktuellem Verstaendnis von IP6-Adressen, muessen es 3 sein)
                        # 
                        if ( ip_adresse_zaehler_trennzeichen != 3 ):
                            return 47 # IP6-Adressteil: IPv4 in IPv6 - Trennzeichenanzahl falsch 

                        # 
                        # Der Zahlenzaehler muss bei einem Ruecksprung in die IP4-Routine
                        # kleiner als 4 sein, da die erste Zahl der IP4-Adresse hier 
                        # schon gelesen worden ist. 
                        # 
                        if ( ip_adresse_zahlen_zaehler > 3 ):
                            return 48 # IP6-Adressteil: IPv4 in IPv6 - zu viele Zeichen im ersten IP4-Block

                        # 
                        # Der Leseprozess wird auf die letzte Trennzeichenposition gestellt.  
                        # Am Schleifenende wird der Leseprozess nochmals um eine Position 
                        # weitergestellt, welches dann die korrekte Position des ersten 
                        # Zeichens der IP4-Adresse ergibt.
                        # 
                        akt_index = position_letzter_punkt # +1 am Schleifenende

                        # 
                        # Sicherstellung, dass die Einbettung der IP4-Adresse mit "ffff" startet.
                        # Es ist hier sichergestellt, dass mindestens 5 Zeichen vor dem Trennzeichen vorhanden sind.
                        # Es muessen 5 Zeichen mindestens vorhanden sein, damit eine IP6-Adresse geparst wird.
                        # 
                        if ( ( pEingabe[ akt_index - 1 ] == 'f' ) and ( pEingabe[ akt_index - 2 ] == 'f' ) and ( pEingabe[ akt_index - 3 ] == 'f' ) and ( pEingabe[ akt_index - 4 ] == 'f' ) ):
                            ()
                            # OK - ffff gefunden
                        
                        else:
              
                            if ( ( pEingabe[ akt_index - 1 ] == 'F' ) and ( pEingabe[ akt_index - 2 ] == 'F' ) and ( pEingabe[ akt_index - 3 ] == 'F' ) and ( pEingabe[ akt_index - 4 ] == 'F' ) ):
                                ()
                                # OK - FFFF gefunden - Wobei die Frage offen bleibt, ob die Grossschreibung hier so in Ordnung ist. 
                            
                            else:
                                return 62 # IP6-Adressteil: IPv4 in IPv6 - falsche Angabe der IP4-Einbettung (Zeichenfolge 'ffff' erwartet)

                        # 
                        # Der Zahlenzaehler wird auf 0 gestellt, da nun eine IP4-Adresse gelesen wird
                        # und der Zahlenzaehler global in dieser While-Schleife benutzt wird.
                        # 
                        ip_adresse_zahlen_zaehler = 0

                        # 
                        # Der Trennzeichenzaehler wird auf 0 gestellt.
                        # 
                        ip_adresse_zaehler_trennzeichen = 0

                        # 
                        # Die Kennzeichenvariable wird auf 2 gestellt, damit der Leseprozess 
                        # in die IP4-Leseroutine verzweigt.
                        # 
                        knz_ipv6 = 2

                    elif ( aktuelles_zeichen == ':' ):
                        # 
                        # Doppel-Punkt (Trennzeichen IP-Adressangaben)
                        # 

                        # 
                        # Anzahl Trennzeichen
                        # Es gibt maximal 8 Bloecke. 
                        # Das ergibt eine maximale Anzahl von 7 Trennzeichen.
                        #    
                        # Es duerfen nicht mehr als 7 Trennzeichen gelesen werden. 
                        # Beim 8ten Trennzeichen, wird der Fehler 42 zurueckgegeben.
                        # 
                        ip_adresse_zaehler_trennzeichen += 1

                        if ( ip_adresse_zaehler_trennzeichen > 8 ):
                            return 42 # IP6-Adressteil: zu viele Trennzeichen, maximal 8 Trennzeichen

                        # 
                        # Es duerfen einmal 2 Doppelpunkte hintereinander kommen.
                        # 

                        # 
                        # Pruefung: 2 Doppelpunkte hintereinander ?
                        # Liegt die letzte Position eines Trennzeichens vor der aktuellen 
                        # Lesepostion, wird der Zaehler fuer aufeinanderfolgende Trennzeichen 
                        # um 1 erhoeht. Dieser Zaehler wird anschliessend auf den Wert 2 
                        # geprueft. Ist der Wert 2, wird der Fehler 50 zurueckgegeben. 
                        # 
                        if ( ( akt_index - position_letzter_punkt ) == 1 ):
                        
                            ip_adresse_anzahl_trennzeichen_hintereinander += 1

                            if ( ip_adresse_anzahl_trennzeichen_hintereinander == 2 ):
                                return 50 # IP6-Adressteil: Es darf nur einmal ein Zweier-Doppelpunkt vorhanden sein.

                        # 
                        # Sind alle Pruefungen fuer einen Punkt durchgefuehrt worden, 
                        # wird die Position des letzten Punktes aktualisiert. 
                        #    
                        # Es wird der Zahlenzaehler und der Wert der aktuellen Zahl auf 0 gestellt.
                        # 
                        position_letzter_punkt = akt_index

                        ip_adresse_zahlen_zaehler = 0

                        ip_adresse_akt_zahl = 0
            
                    elif ( aktuelles_zeichen == ']' ):
            
                        # 
                        # IP6-Adressteil - Abschlusszeichen "]" 
                        # 

                        if ( ip_adresse_zaehler_trennzeichen == 0 ):
                            return 41 # IP6-Adressteil: Trennzeichenanzahl ist 0 

                        # 
                        # Anzahl Trennzeichen
                        # Fuer eine IP6-Adresse muessen mindestens 3 Trennzeichen gelesen worden sein. 
                        # Ist das nicht der Fall, wird der Fehler 43 zurueckgegeben.
                        # 
                        if ( ip_adresse_zaehler_trennzeichen < 3 ):
                            return 43 # IP6-Adressteil: Zu wenig Trennzeichen  

                        # 
                        # Kombination ":]"
                        #    
                        # "first.last@[IPv6:1111:2222:3333::4444:5555:6666:]" 
                        # "first.last@[IPv6:1111:2222:3333:4444:5555:6666::]"
                        #    
                        # - Es darf die Kombination "::" vorkommen, dass nur einmal. 
                        #   Das wird weiter oben geprueft.
                        #    
                        # - Bei der Kombination ":]" kann es sein, dass eben der letzte Wert
                        #   ausgelassen wurde und somit diese Kombination gueltig ist.
                        # 

                        # 
                        # Der letzte Punkt darf nicht auf der vorhergehenden Position 
                        #liegen. Ist das der Fall, wird der Fehler 44 zurueckgegeben. 
                        # 
                        #if ( ( akt_index - position_letzter_punkt ) == 1 ):
                        #    return 44; // IP6-Adressteil: ungueltige Kombination ":]"

                        # 
                        # Das Abschlusszeichen muss auf der letzten Stelle des
                        # Eingabestrings liegen. Ist das nicht der Fall, wird 
                        # 45 als Fehler zurueckgegeben.
                        # 
                        if ( ( akt_index + 1 ) != laenge_eingabe_string ):
                            # 
                            # Nach der IP-Adresse kann noch ein Kommentar kommen. 
                            # Aktuell muss der Kommentar sofort nach dem Abschlusszeichen kommen.
                            # 
                            if ( pEingabe[ akt_index + 1 ] == '(' ):
                
                                # 
                                # Ist das naechste Zeichen nach "]" gleich die oeffnende Klammer,
                                # ist das zeichen OK. Es wird der Leseindex um eine Positon 
                                # verringert.
                                #    
                                # Der Leseprozess wird danach sofort in den Lesevorgang fuer die 
                                # Kommentare gehen.
                                #    
                                # ABC.DEF@[IPv6:1:2:3::5:6:7:8](comment)
                                # 
                                akt_index -= 1

                            elif ( pEingabe[ akt_index + 1 ] == ' ' ):

                                # 
                                # Ist das naechste Zeichen nach "]" ein Leerzeichen, ist der 
                                # Kommentar vom Ende der IP-Adresse durch Leerzeichen getrennt. 
                                # Das Leerzeichen ist OK, der Leseindes wird verringert. 
                                #    
                                # Der Leseprozess wird im naechsten Durchgang das Leerzeichen 
                                # erkennen und in den letzten else-Zweig gefuehrt werden. Dort 
                                # wird erkannt, dass der Leseprozess im Domain-Part ist und wird 
                                # die Leerzeichen ueberspringen.
                                #    
                                # ABC.DEF@[IPv6:1:2:3::5:6:7:8]    (comment)
                                # 
                                akt_index -= 1
                            
                            else:
                            
                                return 45 # IP6-Adressteil: Abschlusszeichen "]" muss am Ende stehen
                            
                            # 
                            # Eine Pruefung auf den Zahlenzaehler bringt nichts. 
                            # Der Zahlenzaehler ist im eventuellen Fehlerfall hier 0. 
                            # Wuerde eine Zahl gelesen, wuerde ein Fehler bei den  
                            # Zahlen geprueft werden.
                            #    
                            # Wuerde versucht werden, den Punkt und das Abschlusszeichen 
                            # mit anderen Zeichen zu trennen, wuerde ein ungueltiges 
                            # Zeichen erkannt werden. 
                            # 
        
                    else:
        
                        return 49 # IP6-Adressteil: Falsches Zeichen in der IP-Adresse
                else:
        
                    # 
                    # Die IP-Adresse besteht nur aus Zahlen und Punkten mit einem 
                    # abschliessendem "]"-Zeichen. Alle anderen Zeichen fuehren 
                    # zu dem Fehler 59 = ungueltiges Zeichen.
                    #    
                    # Es wird nur eine IP4 Adresse geprueft.
                    # 
                    if ( ( ( aktuelles_zeichen >= '0' ) and ( aktuelles_zeichen <= '9' ) ) ):
        
                        # 
                        # Zahlen
                        # - nicht mehr als 3 Ziffern
                        # - nicht groesser als 255 (= 1 Byte)
                        # 

                        # 
                        # Zahlenzaehler
                        # Der Zahlenzaehler wird erhoeht.
                        # Anschliessend wird geprueft, ob schon mehr als 3 Zahlen gelsen wurden. 
                        # Ist das der Fall, wird 53 zurueckgegeben. 
                        # 
                        ip_adresse_zahlen_zaehler += 1

                        if ( ip_adresse_zahlen_zaehler > 3 ):
                            return 53 # IP4-Adressteil: zu viele Ziffern, maximal 3 Ziffern

                        # 
                        # Berechnung Akt-Zahl
                        # Der Wert in der Variablen "akt_zahl" wird mit 10 multipliziert und 
                        # der Wert des aktullen Zeichens hinzugezaehlt. 
                        #    
                        # Der Wert des aktuellen Zeichens ist der Wert des ASCII-Code abzueglich 48.
                        #    
                        # Anschliessend wird geprueft, ob die Zahl groesser als 255 ist. 
                        # Ist die Zahl groesser, wird 54 zurueckgegeben. (Byteoverflow)
                        # 
                        ip_adresse_akt_zahl = ( ip_adresse_akt_zahl * 10 ) + ( ( (int( ord(aktuelles_zeichen)) ) ) - 48 )

                        if ( ip_adresse_akt_zahl > 255 ):
                            return 54 # IP4-Adressteil: Byte-Overflow
                        
                    elif ( aktuelles_zeichen == '.' ):
                        
                        # 
                        # Punkt (Trennzeichen Zahlen)
                        # 

                        # 
                        # Pruefung: Zahlen vorhanden ?
                        #    
                        # Steht der Zahlenzaehler auf 0, wurden keine Zahlen gelesen. 
                        # In diesem Fall wird 55 zurueckgegeben.
                        # 
                        if ( ip_adresse_zahlen_zaehler == 0 ):
                            return 55 # IP4-Adressteil: keine Ziffern vorhanden

                        # 
                        # ANMERKUNG FEHLER 63 
                        # Dieser Fehlercode kann nicht kommen, da bei 2 hintereinanderkommenden 
                        # Punkten keine Zahl gelesen worden sein kann. Dieses ist die  
                        # vorhergehende Pruefung.
                        #    
                        # Es kann auch kein anderes Zeichen gelesen worden sein, das 
                        # wuerde einen anderen Fehler verursachen.
                        # 

                        # 
                        #Pruefung: 2 Punkte hintereinander ?
                        #Die letzte Position eines Punktes, darf nicht vor der aktuellen 
                        #Lesepostion liegen. Ist das der Fall, wird 63 zurueckgegeben.
                        # 
                        #if ( ( akt_index - position_letzter_punkt ) == 1 )
                        #{
                        #  return 63; #IP4-Adressteil: keine 2 Punkte hintereinander
                        #}

                        # 
                        # Anzahl Trennzeichen
                        # Es duerfen nicht mehr als 3 Punkte (=Trennzeichen) gelesen werden. 
                        # Beim 4ten Punkt, wird 56 zurueckgegeben.
                        # 
                        ip_adresse_zaehler_trennzeichen += 1

                        if ( ip_adresse_zaehler_trennzeichen > 3 ):
                            return 56 # IP4-Adressteil: zu viele Trennzeichen

                        # 
                        # Sind alle Pruefungen fuer einen Punkt durchgefuehrt worden, 
                        # wird die Position des letzten Punktes aktualisiert. 
                        #    
                        # Es wird der Zahlenzaehler und der Wert der aktuellen Zahl auf 0 gestellt.
                        # 
                        position_letzter_punkt = akt_index

                        ip_adresse_zahlen_zaehler = 0

                        ip_adresse_akt_zahl = 0
        
                    elif ( aktuelles_zeichen == ']' ):
                    
                        # 
                        # IP4-Adressteil - Abschlusszeichen "]"
                        # 

                        # 
                        # Anzahl Trennzeichen
                        # Fuer eine IP4-Adresse muessen 3 Punkte gelesen worden sein. 
                        # Ist das nicht der Fall, wird 57 zurueckgegeben.
                        # 
                        if ( ip_adresse_zaehler_trennzeichen != 3 ):
                            return 57 # IP4-Adressteil: IP-Adresse Trennzeichenanzahl muss 3 sein 

                        # 
                        # Der letzte Punkt darf nicht auf der vorhergehenden Position 
                        # liegen. Ist das der Fall, wird 58 zurueckgegeben. 
                        # 
                        if ( ( akt_index - position_letzter_punkt ) == 1 ):
                            return 58 # IP4-Adressteil: ungueltige Kombination ".]"

                        # 
                        # Das Abschlusszeichen muss auf der letzten Stelle des
                        # Eingabestrings liegen. Ist das nicht der Fall, wird 
                        # 60 als Fehler zurueckgegeben.
                        # 
                        if ( ( akt_index + 1 ) != laenge_eingabe_string ):
                        
                            # 
                            # Nach der IP-Adresse kann noch ein Kommentar kommen. 
                            # Aktuell muss der Kommentar sofort nach dem Abschlusszeichen kommen.
                            #    
                            # ABC.DEF@[1.2.3.4](comment)
                            # 
                            if ( pEingabe[ akt_index + 1 ] == '(' ):
                                # 
                                # Korrektur des Leseindexes
                                # 
                                akt_index -= 1
            
                            elif ( pEingabe[ akt_index + 1 ] == ' ' ):
            
                                # 
                                # Korrektur des Leseindexes
                                # 
                                akt_index -= 1
            
                            else:
                                return 60 # IP4-Adressteil: Abschlusszeichen "]" muss am Ende stehen

                            # 
                            # Eine Pruefung auf den Zahlenzaehler bringt nichts. 
                            # Der Zahlenzaehler ist im eventuellen Fehlerfall hier 0. 
                            # Wuerde eine Zahl gelesen, wuerde ein Fehler bei den  
                            # Zahlen geprueft werden.
                            #    
                            # Wuerde versucht werden, den Punkt und das Abschlusszeichen 
                            # mit anderen Zeichen zu trennen, wuerde ein ungueltiges 
                            # Zeichen erkannt werden. 
                            # 
                    else:
                        return 59 # IP4-Adressteil: Falsches Zeichen in der IP-Adresse

                akt_index += 1

            # 
            # Pruefung: Abschluss mit ']' ?
            #    
            # Ist die IP-Adressangabe korrekt, steht nach der While-Schleife das abschliessende 
            # Zeichen ']' in der Variablen "aktuelles_zeichen". Ist in der Variablen ein anderes 
            # Zeichen vorhanden, wird der Fehler 61 zurueckgebeben. 
            # 
            if ( aktuelles_zeichen != ']' ):
                return 61 # IP-Adressteil: Kein Abschluss der IP-Adresse auf ']'

            # 
            # Es wurde eine IP-Adresse erkannt, der Wert in der 
            # Variablen "fkt_ergebnis_email_ok" wird um 2 erhoeht.
            # 
            if ( knz_ipv6 == 0 ):
                fkt_ergebnis_email_ok += 2 
            else:
                fkt_ergebnis_email_ok += 4

            # 
            # Index Leseposition nach IP-Adresseinlesung
            #    
            # Bei einer korrekten IP-Adresse, wurde in der While-Schleife die Leseposition um 
            # eine Position zu weit erhoeht. Da die eMail-Adresse in diesem Fall auch korrekt
            # beendet wurde, wird auch in der auesseren While-Schleife die Position nochmals
            # erhoeht. Die aeussere While-Schleife ist aber dann auch beendet. 
            #    
            # Nach der aeusseren While-Schleife kommen keine weiteren Pruefungen auf den 
            # Leseindex, weshalb auf eine Korrektur der Leseposition verzichtet werden kann.
            #    
            # Ist die IP-Adressangabe falsch, wird die innere While-Schleife vorzeitig
            # mit einem Fehlercode verlassen. 
            # 

        elif ( aktuelles_zeichen == '(' ):
      
            # 
            # While-Schleife 4 - Kommentare
            # 
            #    
            # 
            # Kommentare sind am Anfang oder am Ende des Local-Parts erlaubt.
            # Im Domain-Part sind keine Kommentare zugelassen
            # 
            if ( position_at_zeichen > 0 ):
            
                # 
                # Kombination ".(" pruefen Domain-Part.
                # 
                if ( ( position_letzter_punkt > position_at_zeichen ) and ( ( akt_index - position_letzter_punkt ) == 1 ) ):
                    return 102 # Kommentar: Falsche Zeichenkombination ".(" im Domain Part
            
            else:
        
                # 
                # Kombination ".(" pruefen Local Part
                #    
                # Wird eine einleitende Klammer gefunden, darf der letzte Punkt nicht 
                # vor der Klammer liegen. 
                #    
                # Die Position des letzten Punktes muss groesser als 0 sein. Bei weglassen 
                # dieser Pruefung, kommt es zu einem Seiteneffekt mit dem Initialwert 
                # von -1 der Variablen fuer den letzten Punkt. 
                #    
                # Liegt eine falsche Zeichenkombination vor, wird der Fehler 101 zurueckgegeben.
                # 
                if ( ( position_letzter_punkt > 0 ) and ( ( akt_index - position_letzter_punkt ) == 1 ) ):
                    return 101 # Kommentar: Falsche Zeichenkombination ".(" im Local Part

            # 
            # Wurde schon ein Kommentar gelesen, darf kein zweiter Kommentar
            # zugelassen werden. Es wird der Feler 99 zurueckgegeben.
            # 
            if ( position_kommentar_ende > 0 ):
                return 99 # Kommentar: kein zweiter Kommentar gueltig

            # 
            # Innere While-Schleife
            # In einer inneren While-Schleife wird die IP-Adresse geparst und 
            # auf Gueltigkeit geprueft. Die innere While-Schleife laeuft bis
            # zum Stringende der Eingabe.
            # 

            # 
            # Befindet sich der Leseprozess nicht am Anfang der eMail-Adresse, 
            # muss nach dem Abschlusszeichen das AT-Zeichen folgen. 
            #    
            # Kommentart innerhalb des lokalen Parts sind nicht erlaubt. 
            # 
            knz_abschluss_mit_at_zeichen = ( akt_index > 0 )

            knz_abschluss_mit_at_zeichen = ( akt_index == email_local_part_gesamt_start ) == False

            if ( position_at_zeichen > 0 ):
        
                # 
                # Wurde schon ein AT-Zeichen gelesen, darf der Kommentar nicht auf einem AT-Zeichen enden. 
                # 
                knz_abschluss_mit_at_zeichen = False

                # 
                # Sind schon Zeichen nach dem AT-Zeichen gelesen worden, muss der 
                # Kommentar am Stringende enden.
                #    
                # Endet der Kommentar vor dem Stringende, steht der Kommentar mitten 
                # im eMail-String und ist somit falsch.
                # 
                if ( ( akt_index - position_at_zeichen ) > 1 ):
                    knz_kommentar_abschluss_am_stringende = True

            position_kommentar_start = akt_index

            akt_index += 1

            aktuelles_zeichen = 'A'

            while ( ( akt_index < laenge_eingabe_string ) and ( aktuelles_zeichen != ')' ) ):
        
                # 
                # Aktuelles Pruefzeichen
                # Das aktuelle Zeichen wird aus der Eingabe am aktuellen Index herausgelesen. 
                # 
                aktuelles_zeichen = pEingabe[ akt_index ]

                # 
                # Alle erlaubten Stringzeichen werden durchgelassen. 
                # Falsche Zeichen erzeugen einen Fehler.
                # 

                if ( ( ( aktuelles_zeichen >= 'a' ) and ( aktuelles_zeichen <= 'z' ) ) or ( ( aktuelles_zeichen >= 'A' ) and ( aktuelles_zeichen <= 'Z' ) ) ):
                    ()
                    # OK - Buchstaben
          
                elif ( ( aktuelles_zeichen >= '0' ) and ( aktuelles_zeichen <= '9' ) ):
                    ()
                    # OK - Zahlen
          
                elif ( ( aktuelles_zeichen == '_' ) or ( aktuelles_zeichen == '-' ) or ( aktuelles_zeichen == '@' ) or ( aktuelles_zeichen == '.' ) or ( aktuelles_zeichen == ' ' ) or ( aktuelles_zeichen == '!' ) or ( aktuelles_zeichen == '#' ) or ( aktuelles_zeichen == '$' ) or ( aktuelles_zeichen == '%' ) or ( aktuelles_zeichen == '&' ) or ( aktuelles_zeichen == '\'' ) or ( aktuelles_zeichen == '*' ) or ( aktuelles_zeichen == '+' ) or ( aktuelles_zeichen == '-' ) or ( aktuelles_zeichen == '/' ) or ( aktuelles_zeichen == '=' ) or ( aktuelles_zeichen == '?' ) or ( aktuelles_zeichen == '^' ) or ( aktuelles_zeichen == '`' ) or ( aktuelles_zeichen == '{' ) or ( aktuelles_zeichen == '|' ) or ( aktuelles_zeichen == '}' ) or ( aktuelles_zeichen == '~' ) ):
                    ()
                    # OK - Sonderzeichen
          
                elif ( aktuelles_zeichen == ')' ):
                    
                    # OK - abschliessendes Anfuehrungszeichen 

                    # 
                    # Der Leseprozessindex muss nach der While-Schleife auf dem jetzt
                    # gerade gueltigen Index stehen. 
                    #    
                    # Am Ende dieser inneren While-Schleife wird der Leseprozess um 
                    # eine Position weiter gestellt. Der Leseprozessindex wird zum 
                    # Ausgleich hier um eine Position verringert.
                    #    
                    # Die aeussere While-Schleife erhoeht schlussendlich den Leseprozess, 
                    # damit dieser dann auf das Zeichen nach dem hier gefundenen 
                    # Anfuehrungszeichen verarbeiten kann. 
                    # 
                    akt_index -= 1
          
                elif ( aktuelles_zeichen == '\\' ):

                    # 
                    # Maskiertes Zeichen 
                    # Der Leseprozess muss nach naechste Zeichen pruefen. 
                    # Der Leseprozessindex wird um ein Zeichen weiter gestellt.
                    # 
                    akt_index += 1

                    # 
                    # Pruefung: Stringende ?
                    # 
                    if ( akt_index == laenge_eingabe_string ):
                        return 96 # Kommentar: Escape-Zeichen nicht am Ende der Eingabe

                    # 
                    # Zeichen nach dem Backslash lesen. 
                    # Das Zeichen darf ein Backslash oder ein Anfuehrungszeichen sein. 
                    # Alle anderen Zeichen fuehren zum Fehler 91.
                    # 
                    aktuelles_zeichen = pEingabe[ akt_index ]

                    if ( ( aktuelles_zeichen != '\\' ) and ( aktuelles_zeichen != '"' ) ):
                        return 91 # Kommentar: Ungueltige Escape-Sequenz im Kommentar

                else:
                    
                    # 
                    # Fehler 92
                    # Dieser Fehler wird zurueckgegeben, wenn ein ungueltiges 
                    # Zeichen im Kommentar vorhanden ist.
                    # 
                    return 92 # Kommentar: Ungueltiges Zeichen im Kommentar

                # 
                # Der Leseprozessindex wird um eine Position weitergestellt.
                # 
                akt_index += 1

            # 
            # Pruefung: Wurde eine abschliessende Klammer gefunden ? 
            #    
            # Nach der While-Schleife muss die Variablen "aktuelles_zeichen" eine 
            # abschliessende Klammer sein. Nur dann wurde die Einleseschleife 
            # korrekt beendet. 
            #    
            # Steht ein anderes Zeichen in der Variablen, ist der Leseprozess 
            # am Stringende der Eingabe angekommen. Das ist die zweite Moeglichkeit, 
            # wie die While-Schleife beendet werden kann. 
            # 
            if ( aktuelles_zeichen != ')' ):
                return 93 # Kommentar: kein abschliessendes Zeichen fuer den Komentar gefunden. ')' erwartet

            # 
            # Pruefung: Leseprozess am Stringende angelangt ?
            #    
            # Wurde die While-Schleife korrekt beendet, kann es sein, dass die 
            # abschliessende Klammer am Stringende steht.  
            # 
            if ( akt_index + 1 >= laenge_eingabe_string ):

                if ( position_at_zeichen > 0 ):
                    ()
                    # 
                    # Im Domain-Part darf der Kommentar am Stringende aufhoeren
                    # 
                else:
                    return 95 # Kommentar: Der Kommentar endet am Stringende (Vorzeitiges Ende der Eingabe)
        
            else:
                # 
                # Pruefung: naechstes Zeichen gleich AT-Zeichen ?
                # 
                if ( pEingabe[ akt_index + 1 ] == '@' ):
                
                    if ( knz_abschluss_mit_at_zeichen == False ):
                        return 98 # Kommentar: Kein lokaler Part vorhanden
                
                elif ( pEingabe[ akt_index + 1 ] == '.' ):
                    return 103 # Kommentar: Falsche Zeichenkombination ")."
                
                else:
                
                    if ( knz_abschluss_mit_at_zeichen ):
                        return 97 # Kommentar: Nach dem Kommentar muss ein AT-Zeichen kommen

                if ( knz_kommentar_abschluss_am_stringende ):
                    return 100 # Kommentar: Kommentar muss am Strinende enden

            # 
            # Die Position der abschliessenden Klammer wird gespeichert. 
            # 
            position_kommentar_ende = akt_index

            # 
            # Leerzeichen nach Kommentar ----------------------------------------------------------------------
            #    
            # Nach dem Kommentar koennen noch weitere Leerzeichen bis zur eMail-Adresse folgen.
            # Diese Leerzeichen werden mittels einer While-Schleife ueberlesen.
            #    
            #     "(spaces after comment)     name1.name2@domain1.tld"
            # 
            if ( ( akt_index + 1 < laenge_eingabe_string ) and ( position_at_zeichen <= 0 ) ):

                if ( pEingabe[ akt_index + 1 ] == ' ' ):
          
                    # 
                    # aktuelles Zeichen konsumieren, bzw. Leseposition 1 weiterstellen
                    # 
                    akt_index += 1

                    # 
                    # Ueberlese alle Leerzeichen in einer While-Schleife. 
                    # 
                    while ( ( akt_index < laenge_eingabe_string ) and ( pEingabe[ akt_index ] == ' ' ) ):
                    
                        akt_index += 1
            
                    # 
                    # Am Schleifenende wird die Leseposition erhoeht. 
                    # Es wurde in dieser Bedingung fuer das Ueberlesen von Leerzeichen, der 
                    # aktuelle Index um eine Position zu weit erhoeht. Dass muss korrigiert 
                    # werden. Daher wird der aktuelle Index um 1 vermindert.
                    # 
                    akt_index -= 1
            # 
            # Leerzeichen nach Kommentar ----------------------------------------------------------------------
            # 
 
        else:
            # 
            # Sonderbedingung: Leerzeichentrennung bis Kommentar im Domain-Part
            #    
            # "email@domain.com (joe Smith)"
            #    
            # Ist das aktuelle Zeichen ein Leerzeichen und der Leseprozess befindet 
            # sich im Domainpart (position_at_zeichen > 0), dann muss geprueft werden, 
            # ob nach den Leerzeichen eine oeffnende Klammer kommt.
            # 
            if ( ( aktuelles_zeichen == ' ' ) and ( position_at_zeichen > 0 ) ):
            
                # 
                # aktuelles Zeichen konsumieren, bzw. Leseposition 1 weiterstellen
                # 
                akt_index += 1

                # 
                # Ueberlese alle Leerzeichen in einer While-Schleife. 
                # 
                while ( ( akt_index < laenge_eingabe_string ) and ( pEingabe[akt_index ] == ' ' ) ):
                    akt_index += 1

                # 
                # Wurde in der While-Schleife bis zum Eingabeende gelesen, 
                # wird der Fehler 22 zurueckgegeben, da das Leerzeichen 
                # falsch ist.
                # 
                if ( akt_index == laenge_eingabe_string ):
                    return 22

                # 
                # Nach der While-Schleife muss das Zeichen an der aktuellen 
                # Leseposition eine oeffnende Klammer sein. Alle anderen 
                # Zeichen fuehren zu einem Fehler, da das einleitende
                # Leerzeichen ein falsches Zeichen war. Es wird in diesem 
                # Fall der Fehler 105 zurueckgegeben. 
                # 
                if ( pEingabe[akt_index ] == '[' ):
                    # return 106 # Kommentar: Leerzeichentrennung im Domain-Part. 

                    akt_index -= 1
                    
                elif ( pEingabe[akt_index ] != '(' ):
                    return 105 # Kommentar: Leerzeichentrennung im Domain-Part. Oeffnende Klammer erwartet
                
                else:
                    # 
                    # In der While-Schleife wurde die Leseposition einmal zu viel erhoeht.
                    # Die Leseposition wird um eine Position verringert.
                    # Da sich der Leseprozess im Domain-Part befindet gibt es ein vorhergehendes Zeichen.
                    # 
                    akt_index -= 1
            else:

                return 22 # Zeichen: ungueltiges Zeichen in der Eingabe gefunden
        
        akt_index += 1

    # 
    # Pruefungen nach der While-Schleife    
    # 

    # 
    # Pruefung: Punkt gefunden ?
    # Bei einer IP-Adressangabe OK, da auch dort Punkte gefunden werden muessen.
    # Bei einer IP6-Adressangabe wird die Variable "position_letzter_punkt" fuer 
    # die Doppelpunkte ":" in der Adressangabe benutzt. 
    # 
    if ( ( position_letzter_punkt == -1 ) or ( position_letzter_punkt == position_at_zeichen ) ):
        return 34 # Trennzeichen: keinen Punkt gefunden (Es muss mindestens ein Punkt fuer den Domain-Trenner vorhanden sein)

    # 
    # Pruefung: AT-Zeichen gefunden ?
    # Ist der Wert der Variablen "position_at_zeichen" gleich -1, wurde kein AT-Zeichen 
    # gefunden. Es wird der Fehler 28 zurueckgegeben.
    #   
    # Bei einer IP-Adressangabe OK, da auch dort ein AT-Zeichen vorhanden sein muss.
    # 
    if ( position_at_zeichen == -1 ):
        return 28 # AT-Zeichen: kein AT-Zeichen gefunden

    # 
    # Pruefung: EMail-Adresse ohne IP-Adressangabe ?
    #    
    # Handelt es sich um eine eMail-Adresse ohne IP-Adresse, ist der Wert in der 
    # Variablen "fkt_ergebnis_email_ok" kleiner als 2. 
    #    
    # Wenn dem so ist, muessen noch Abschlusspruefungen bezueglich des letzten 
    # Punktes gemacht werden.
    # 
    if ( fkt_ergebnis_email_ok < 2 ):
        # 
        # Pruefung: Letzter Punkt nach AT-Zeichen ?
        # Die Position des letzten Punktes muss groesser sein als die Position 
        # des AT-Zeichens. Ist die Punkt-Position kleiner als die Position des 
        # AT-Zeichens wird der Fehler 35 zurueckgegeben.
        #    
        # Bei einer IP-Adressangabe OK, da dort die gleichen Bedingungen gelten.
        # 
        if ( position_letzter_punkt < position_at_zeichen ):
            return 35 # Trennzeichen: der letzte Punkt muss nach dem AT-Zeichen liegen (... hier eben die negative Form, wenn der letzte Punkt vor dem AT-Zeichen stand ist es ein Fehler)

        # 
        # Pruefung: Letzter Punkt gleich Stringende ?
        # Die Position des letzten Punktes darf nicht am Stringende liegen. 
        # Liegt der letzte Punkt am Stringende, wird der Fehler 36 zurueckgegeben.
        #    
        # Bei einer IP-Adressangabe OK, da dort die gleichen Bedingungen gelten.
        # 
        if ( ( position_letzter_punkt + 1 ) == laenge_eingabe_string ):
            return 36 # Trennzeichen: der letzte Punkt darf nicht am Ende liegen

        laenge_tld = 0

        if ( ( position_letzter_punkt > position_at_zeichen ) and ( position_kommentar_start > position_letzter_punkt ) ):
            #laenge_tld = position_kommentar_start - position_letzter_punkt;
            laenge_tld = 2 # pEingabe.substring( position_letzter_punkt, position_kommentar_start ).trim().length()
      
        else:
            laenge_tld = laenge_eingabe_string - ( position_letzter_punkt + 1 )

        # 
        # https://stackoverflow.com/questions/15537384/email-address-validation-of-top-level-domain
        # 
        if ( laenge_tld < 2 ):
            return 14 # Laenge: Top-Level-Domain muss mindestens 2 Stellen lang sein.

        # 
        # https://stackoverflow.com/questions/9238640/how-long-can-a-tld-possibly-be/9239264
        # 
        if ( laenge_tld > 63 ):
            return 15 # Laenge: Top-Level-Domain darf nicht mehr als 63-Stellen lang sein.

        # 
        # https://stackoverflow.com/questions/9071279/number-in-the-top-level-domain
        # 

        aktuelles_zeichen = pEingabe[ position_letzter_punkt + 1 ]

        if ( ( aktuelles_zeichen >= '0' ) and ( aktuelles_zeichen <= '9' ) ):
            return 23 # Zeichen: Top-Level-Domain darf nicht mit Zahl beginnen

        # if ( zahlen_zaehler > 0 ) { return 19; } // Laenge: Top-Level-Domain darf keine Zahlen haben ... oder doch ?

    return fkt_ergebnis_email_ok
