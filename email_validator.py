
def validateEmail( pEingabe = '' ):
   
    fkt_ergebnis = 0
   
    '''
    Pruefung: Eingabelaenge gleich 0 ?

    Es wird kein Trim gemacht, da ein Trim Zeit verbrauchen wuerde.
    Diese Funktion soll den String so pruefen, wie dieser uebergeben wurde.
    Es ist nicht die Aufgabe dieser Funktion, die Eingabe zu manipulieren.
    Besteht die Eingabe nur aus Leerzeichen, wird beim ersten Leerzeichen
    ein ungueltiges Zeichen erkannt und der Fehler 29 zurueckgegeben.

    Ist die Eingabe ohne Trim schon ein Leerstring, wird der
    Fehler 11 zurueckgegeben.
    '''
    
    if ( len( pEingabe ) == 0 ):
        return 10
   
    '''
    Laenge Eingabestring
    Die Variable "laenge_eingabe_string" bezeichnete in der ersten Version 
    die tatsaechliche Laenge des Eingabestrings. Durch den Einbau der Pruefroutine
    fuer eckige Klammern, kann der Inhalt aber auch die Bedeutung einer 
    Positonsangabe haben. 
    '''
    laenge_eingabe_string = len( pEingabe )

    '''
    Generell darf die Eingabe nicht laenger als 255 Zeichen sein.
    Die Pruefung auf die minimale Laenge der eMail-Adresse folgt weiter unten.
    '''
    if ( laenge_eingabe_string > 255 ):
        return 12
    
    '''
    Position AT-Zeichen
    Initialwert -1 steht fuer "kein AT-Zeichen gefunden"
    '''
    position_at_zeichen = -1

    '''
    Merker "letzte Position eines Punktes"
    Initialwert -1 steht fuer "keinen Punkt gefunden"
    '''
    position_letzter_punkt = -1

    '''
    Speichert die Position des zuletzt gefundenen Anfuehrungszeichens. 
    Start- oder Endzeichen. 
    '''
    position_anf_zeichen_akt = -1

    '''
    Speichert die Position der letzten geschlossenen Klammer ')' eines gueltigen Kommentares. 
    '''
    position_kommentar_ende = -1

    position_kommentar_start = -1

    '''
    Zaehler fuer Zeichen zwischen zwei Trennzeichen.
    Die Trennzeichen sind Punkt und AT-Zeichen
    '''
    zeichen_zaehler = 0

    '''
    Start Leseposition
    Die Startposition fuer die While-Schleife ist hier 0. Das ist
    das erste Zeichen der Eingabe. 

    Bei eMail-Adressen in spitzen Klammern ist die Startposition 
    immer die Position nach der oeffnenden eckigen Klammer.
    '''
    akt_index = 0

    aktuelles_zeichen = ' '

    email_local_part_start = 0
    email_domain_part_ende = laenge_eingabe_string - 1

    '''
    Berechnung der Laenge der reinen eMail-Adressangabe.
    
    Die Variable "akt_index" steht hier auf dem ersten Zeichen der eMail-Adresse. 
    Die Variable "laenge_eingabe_string" steht nach dem letzten zu pruefenden 
    Zeichen der eMail-Adresse. Dieses um mit der bisherigen Variablenbezeichnung 
    konform zu sein, welches die Laenge des Eingabestrings war. 
    '''
    zeichen_zaehler = laenge_eingabe_string - akt_index

    '''
    http://de.wikipedia.org/wiki/E-Mail-Adresse
    Innerhalb von RFC 5322 gibt es keine Laengenbegrenzung fuer eMail-Adressen. 
    
    Im RFC 5321 wird die maximale Laenge des Local-Parts mit 64 Bytes und
    die maximale Laenge des Domainnamens mit 255 Bytes angegeben. Zusammen 
    mit dem "@"-Zeichen ergaebe sich daraus die maximale Laenge einer 
    E-Mail-Adresse von 320 Bytes. 
    
    Im RFC 5321 wird auch die maximale Laenge des "Path"-Elements definiert, 
    welches die Elemente "FROM" und "RCPT TO" im Envelope bestimmt und die 
    maximale Laenge von Bytes einschliesslich der Separatoren "<" und ">" hat. 
    Daraus ergibt sich eine maximale Laenge der E-Mail-Adresse von 254 Bytes 
    einschliesslich des "@". Eine E-Mail mit einer laengeren Adresse, kann 
    ueber RFC-konforme SMTP-Server weder verschickt noch empfangen werden.
    
    Minimal moegliche eMail-Adresse ist "A@B.CD", gleich 6 Stellen.
    '''
    if ( ( zeichen_zaehler < 6 ) or ( zeichen_zaehler > 254 ) ):
        return 12 # Laenge: Laengenbegrenzungen stimmen nicht 

    zeichen_zaehler = 0

    '''
    Variable "fkt_ergebnis_email_ok"
    
    Speicherung des Funktionsergebnisses fuer korrekte eMail-Angaben. 
    
    Ist die eMail-Adresse rein Text ohne Sonderformen, bleibt der Wert auf 0.
    
    Ist im Local-Part ein String vorhanden, wird der Wert auf 1 geaendert.
    
    Ist eine IP4-Adressangabe vorhanden, wird der Wert um 2 erhoeht.
    
    Ist eine IP6-Adressangabe vorhanden, wird der Wert um 4 erhoeht.
    
    Ist ein Kommentar vorhanden, wird der Rueckgabewert konvertiert.
    
    Es werden nur die unten stehenden 10 Ergebniswerte geliefert, 
    damit korrekte eMail-Adressen unter dem Wert 10 bleiben.
    
    Bezueglich der Erhoehung des Wertes bei einer Stringangabe ist es 
    so, dass die IP-Adresse erst nach dem AT-Zeichen korrekt erkannt
    wird. Eine korrekt gelesene String-Angabe wird immer vor einer 
    moeglichen IP-Adresse gelesen werden und somit wird der Ergebnis-
    wert auf 1 gestellt, bevor die Erhoehung bei der IP-Adresse 
    gemacht werden kann.   
    
    Folgende Ergebnisse sind moeglich:
    
     0 = eMail-Adresse korrekt
     1 = eMail-Adresse korrekt (Local Part mit String)
     2 = eMail-Adresse korrekt (IP4-Adresse)
     3 = eMail-Adresse korrekt (Local Part mit String und IP4-Adresse)
     4 = eMail-Adresse korrekt (IP6-Adresse)
     5 = eMail-Adresse korrekt (Local Part mit String und IP6-Adresse)
     6 = eMail-Adresse korrekt (Kommentar)
     7 = eMail-Adresse korrekt (Kommentar, String)
     8 = eMail-Adresse korrekt (Kommentar, String, IP4-Adresse)
     9 = eMail-Adresse korrekt (Kommentar, String, IP6-Adresse)
     
    Durch die verschiedenen Rueckgabewerte, kann der Aufrufer eMail-Adressen 
    mit IP-Adresse oder String-Teilen im Nachgang noch abweisen.  
    '''
    fkt_ergebnis_email_ok = 0

    knz_kommentar_abschluss_am_stringende = False

    if ( ( laenge_eingabe_string < 6 ) or ( laenge_eingabe_string > 254 ) ):
        return 12 # Laenge: Laengenbegrenzungen stimmen nicht

    email_local_part_gesamt_start = akt_index
    
    '''
    While-Schleife 1
    
    In der aeusseren While-Schleife wird eine grundlegende eMail-Adressstruktur geparst. 
    '''
    while ( akt_index < laenge_eingabe_string ):
        
        aktuelles_zeichen = pEingabe[ akt_index ]
        
        #print(f' {akt_index} {aktuelles_zeichen}')

        '''
        Bedingungen Zeichen A-Z, a-z und Zahlen
        '''
        if ( ( ( aktuelles_zeichen >= 'a' ) and ( aktuelles_zeichen <= 'z' ) ) or ( ( aktuelles_zeichen >= 'A' ) and ( aktuelles_zeichen <= 'Z' ) ) or ( ( aktuelles_zeichen >= '0' ) and ( aktuelles_zeichen <= '9' ) ) ):
            '''
            Buchstaben ("A" bis "Z" und "a" bis "z") und Zahlen duerfen an jeder Stelle der eMail-Adresse vorkommen.

            Ein solches Zeichen kann selber keinen Fehler produzieren.
           
            Es wird der Zeichenzaehler um eins erhoeht.
            '''
            zeichen_zaehler += 1
            
        elif ( ( aktuelles_zeichen == '_' ) or ( aktuelles_zeichen == '-' ) ):
      
            '''
            Im Domain-Part duerfen die Sonderzeichen '_' und '-' nicht am Start stehen.  
            
            Steht der Zeichenzaehler auf 0, steht das aktuelle Zeichen an einer ungueltigen Position.
            
            Nach RFC 952 darf im Domain-Part kein Teilstring mit einer Zahl oder einem Punkt starten.
            Nach RFC 1123 duerfen Hostnamen mit Zahlen starten.


            https://verifalia.com/help/email-validations/can-email-addresses-have-hyphens-minus-signs-dashes
            
            Placement - email addresses cannot have a hyphen (or minus sign, or dash) as the first or last letter in 
            the domain part. Similarly, the hyphen cannot be placed directly in front of or following, the dot (.). 
            Have a look at some examples of correct vs. incorrect use:
            
            Correct
            
            username@exam-ple.com
            username@e-xample.com
            
            Incorrect
            
            username@example-.com
            username@-example.com
            '''
            if ( akt_index == email_local_part_start ):
            
                if ( pEingabe[ akt_index + 1 ] == '\"' ):
                    return 140 # Trennzeichen: ungueltige Zeichenkombination -"

                if ( pEingabe[ akt_index + 1 ] == '(' ):
                    return 141 # Trennzeichen: ungueltige Zeichenkombination -(

            '''
            Pruefung: Befindet sich der Leseprozess im Domain-Part ?
             
            Im Domain-Part ist der Leseprozess, wenn die Position des At-Zeichens groesser als 0 ist.
            '''
            if ( position_at_zeichen > 0 ):
        
                if ( zeichen_zaehler == 0 ):
                    return 20 # Zeichen: Zahl oder Sonderzeichen nur nach einem Buchstaben (Teilstring darf nicht mit Zahl oder Sonderzeichen beginnen)

                if ( ( akt_index + 1 ) == laenge_eingabe_string ):
                    return 24 # Zeichen: Kein Sonderzeichen am Ende der eMail-Adresse
                
                else:

                    '''
                    https://en.wikipedia.org/wiki/Email_address
                    
                    Domain-Part:
                    hyphen -, provided that it is not the first or last character.
                    '''
                    if ( pEingabe[ akt_index + 1 ] == '.' ):
                        return 20 # Trennzeichen: ungueltige Zeichenkombination "-."

        elif ( aktuelles_zeichen == '.' ):

            '''
            Bedingungen fuer einen Punkt
            '''
      
            '''
            Pruefung: Wurde schon ein Punkt gefunden?
             
            Nein, wenn in der Speichervariablen "position_letzter_punkt" noch der Initialwert von -1 steht.
            '''
            if ( position_letzter_punkt == -1 ):
            
                '''
                Pruefung: Leseposition gleich 0 ?
                 
                Ist der aktuelle Index gleich 0 und das aktuelle Zeichen ein Punkt,
                wird der Fehler 30 zurueckgegeben. 
                 
                Es darf nicht mit dem Zeichenzaehler geprueft werden, da der erste 
                Local-Part auch ein String sein kann. Dort wird der Zeichenzaehler 
                nicht erhoeht.
                '''
                if ( akt_index == ( position_kommentar_ende + 1 ) ):
                    return 30 # Trennzeichen: kein Beginn mit einem Punkt

                '''
                Der erste Punkt darf nicht am gespeicherten Beginn der eMail-Adresse liegen. 
                Wichtig bei Eckigen-Klammern, bei welchen die eMail-Adresse nicht am 
                Index 0 beginnt.
                '''
                if ( akt_index == email_local_part_start ):
                    return 142 # Trennzeichen: kein Beginn mit einem Punkt
            else:
                '''
                Pruefung: Zwei Punkte hintereinander ?
                 
                Ist die Differenz von der aktuellen Leseposition und der letzten 
                Punkt-Position gleich 1, stehen 2 Punkte hintereinander. Es wird 
                in diesem Fall der Fehler 31 zurueckgegeben.
                '''
                if ( ( akt_index - position_letzter_punkt ) == 1 ):
                    return 31 # Trennzeichen: keine zwei Punkte hintereinander

            if ( position_at_zeichen > 0 ):
                '''
                Domain-Part-Labellaenge
                https://de.wikipedia.org/wiki/Hostname
                https://en.wikipedia.org/wiki/Hostname
                
                Ein Domain-Label muss 1 Zeichen umfassen und darf maximal 63 Zeichen lang sein. 
                Bei der Berechnung wird auf 64 Zeichen geprueft, da so die Subtraktion nicht 
                verkompliziert werden muss (es wird die Position des letzten Punktes mitgezaehlt).
                
                Es muss hier der Index fuer den eigentlichen eMail-Start beruecksichtigt werden. 
                Normalerweise startet die eMail-Adresse bei Index 0. Bei eMail-Adressen mit 
                spitzen Klammern kann der Start spaeter sein.
                
                Ist der aktuelle Domain-Label zu lang, wird der Fehler 63 zurueckgegeben.
                '''
                if ( ( akt_index - position_letzter_punkt ) > email_local_part_start + 64 ):
                    return 63 # Domain-Part: Domain-Label zu lang (maximal 63 Zeichen)

            '''
            Index des letzten Punktes speichern
            '''
            position_letzter_punkt = akt_index

            '''
            Zeichen- und Zahlenzaehler nach einem Punkt auf 0 stellen
            '''
            zeichen_zaehler = 0

        elif ( aktuelles_zeichen == '@' ):
            '''
            Bedingungen fuer das AT-Zeichen
            '''

            '''
            Pruefung: Position AT-Zeichen ungleich -1 ?
            
            Wurde bereits ein AT-Zeichen gefunden, ist in der Positionsvariablen 
            ein Wert groesser 0 vorhanden. Es darf im Leseprozess nur einmal 
            ein (unmaskiertes) AT-Zeichen als Trennerzeichen gefunden werden. 
            Ist schon eine AT-Zeichenposition vorhanden, wird der Fehler
            29 zurueckgegeben. 
            
            Wurde noch kein AT-Zeichen gefunden, werden weitere Pruefungen gemacht. 
            '''
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
        
            '''
            Kombination "@."
            An dieser Position ist sichergestellt, dass in der Eingabe noch 
            mindestens 1 Zeichen folgt. Es gibt hier keine Index-Out-Of-Bounds Exception.
             
            Ansonsten wuerde das AT-Zeichen am Ende stehen und der Aufrufer 
            wuerde 8 als Funktionsergebnis bekommen.
            '''
            if ( pEingabe[ akt_index + 1 ] == '.' ):
                return 33 # Trennzeichen: ungueltige Zeichenkombination "@."

            '''
            Position des AT-Zeichens merken
            '''
            position_at_zeichen = akt_index

            '''
            Zeichenzaehler nach dem AT-Zeichen auf 0 stellen
            '''
            zeichen_zaehler = 0

            '''
            Position letzer Punkt
            
            Das AT-Zeichen trennt den Local- und Domain-Part. 
            Die Position des letzen Punkts muss ausgenullt werden, um 
            Seiteneffekte bei der Laengenberechnung der einzelnen 
            Domain-Parts zu vermeiden.
            
            Der Domain-Part startet am AT-Zeichen und auf dessen Index 
            wird auch die Position des letzten Punktes gesetzt.
            '''
            position_letzter_punkt = akt_index
            
        elif ( aktuelles_zeichen == '\\' ):
            '''
            Sonderzeichen mit Qoutierung, welche nur im Local-Part vorkommen duerfen
             
            \ @
             
            Ist die Positon fuer das AT-Zeichen groesser als 0, befindet sich 
            der Leseprozess im Domain-Part der eMail-Adresse. Dort sind diese 
            Zeichen nicht erlaubt und es wird 21 zurueckgegeben.
            '''
            if ( position_at_zeichen > 0 ):
                return 21 # Zeichen: Sonderzeichen im Domain-Part nicht erlaubt
        

            '''
            Maskiertes Zeichen 
            Der Leseprozess muss noch das naechste Zeichen pruefen. 
            Der Leseprozessindex wird um ein Zeichen weiter gestellt.
            '''
            akt_index += 1

            '''
             Pruefung: Stringende ?
            '''
            if ( akt_index == laenge_eingabe_string ):
                return 83 # String: Escape-Zeichen nicht am Ende der Eingabe

            '''
            Zeichen nach dem Backslash lesen. 
            Das Zeichen darf ein Backslash oder ein Anfuehrungszeichen sein. 
            Alle anderen Zeichen fuehren zum Fehler 84.
            '''
            aktuelles_zeichen = pEingabe[ akt_index ]

            if ( ( aktuelles_zeichen != '\\' ) and ( aktuelles_zeichen != '@' ) and ( aktuelles_zeichen != ' ' ) and ( aktuelles_zeichen != '\'' ) ):
                return 84 # String: Ungueltige Escape-Sequenz im String
            
            aktuelles_zeichen = 'A'
        
        elif ( ( aktuelles_zeichen == '!' ) or ( aktuelles_zeichen == '#' ) or ( aktuelles_zeichen == '$' ) or ( aktuelles_zeichen == '%' ) or ( aktuelles_zeichen == '&' ) or ( aktuelles_zeichen == '\'' ) or ( aktuelles_zeichen == '*' ) or ( aktuelles_zeichen == '+' ) or ( aktuelles_zeichen == '-' ) or ( aktuelles_zeichen == '/' ) or ( aktuelles_zeichen == '=' ) or ( aktuelles_zeichen == '?' ) or ( aktuelles_zeichen == '^' ) or ( aktuelles_zeichen == '`' ) or ( aktuelles_zeichen == '{' ) or ( aktuelles_zeichen == '|' ) or ( aktuelles_zeichen == '}' ) or ( aktuelles_zeichen == '~' ) ):
            '''
               asc("!") = 033   asc("*") = 042 
               asc("#") = 035   asc("+") = 043 
               asc("$") = 036   asc("-") = 045 
               asc("%") = 037   asc("/") = 047
               asc("&") = 038 
               asc("'") = 039
               
               asc("=") = 061   asc("{") = 123 
               asc("?") = 063   asc("|") = 124 
               asc("^") = 094   asc("}") = 125 
               asc("_") = 095   asc("~") = 126 
               asc("`") = 096   asc(" ") = 032 
            '''

            '''
            Sonderzeichen, welche nur im Local-Part vorkommen duerfen
             
            !#$%&'*+-/=?^_`{|}~
             
            Ist die Positon fuer das AT-Zeichen groesser als 0, befindet sich 
            der Leseprozess im Domain-Part der eMail-Adresse. Dort sind diese 
            Zeichen nicht erlaubt und es wird 21 zurueckgegeben.
            '''
            if ( position_at_zeichen > 0 ):
                return 21 # Zeichen: Sonderzeichen im Domain-Part nicht erlaubt

        elif ( aktuelles_zeichen == '"' ):
        
            '''
            While-Schleife 2 - String
            '''

            '''
            Pruefung: Leseprozess im Domain-Part ?
            Im Domain-Part sind keine Anfuehrungszeichen erlaubt. 
            Es wird der Fehler 82 zurueckgegeben.
            '''
            if ( position_at_zeichen > 0 ):
                return 82 # String: kein Anfuehrungszeichen nach dem AT-Zeichen

            '''
            Pruefung: Zeichenkombination ."
            
            Ein lokaler Part in Anfuehrungszeichen muss nach einem Trennzeichen starten.
            
            Wurde schon ein Punkt gefunden und die Differenz des Leseprozesses 
            ist nicht 1, wird der Fehler 81 zurueckgegeben.
            '''
            if ( position_letzter_punkt > 0 ):
                if ( akt_index - position_letzter_punkt != 1 ):
                    return 81 # String: Ein startendes Anfuehrungezeichen muss direkt nach einem Punkt kommen

            '''
            Pruefung: Start mit Anfuehrungszeichen 
            Ein Anfuehrungszeichen darf nur am Beginn eines Blockes kommen. 
            Wurden im aktuellem Block schon zeichen gelesen, ist ein startendes Anfuehrungszeichen
            falsch gesetzt. Es wird der Fehler 80 zurueckgegeben.
           
            anders:
           
            Der Zeichenzaehler muss fuer den aktuellen Block 0 sein. Der Zeichenzaeler ist 
            fuer den aktuellen Block 0 am Start oder nach einem Punkt.
           
            '''
            if ( zeichen_zaehler > 0 ):
                return 80 # String: Ein startendes Anfuehrungszeichen muss am Anfang kommen, der Zeichenzaehler darf nicht groesser als 0 sein

            '''
            Das aktuelle Zeichen ist hier noch ein Anfuehrungszeichen. 
            Die nachfolgende While-Schleife wuerde nicht starten, wenn 
            das Zeichen nicht geaendert wuerde. Darum wird der Variablen 
            "aktuelles_zeichen" das Zeichen 'A' zugewiesen.
            '''
            aktuelles_zeichen = 'A'

            '''
            Position des aktuellen Anfuehrungszeichens merken
            '''
            position_anf_zeichen_akt = akt_index

            '''
            Der Leseprozess wird um ein Zeichen weitergestellt. 
            Damit wird das einleitende Anfuehrungszeichen vom Parser verarbeitet.
            
            Steht das einleitende Anfuehrungszeichen am Stringende, wird die 
            While-Schleife nicht ausgefuehrt, da die Variable "akt_index" jetzt 
            gleich der Laenge des Eingabestrings ist. Die Differenz zur 
            gespeicherten Position des einleitenden Anfuehrungszeichens ist 1. 
            Das ist die erste Pruefung nach der While-Schleife. Es werden 
            somit Eingaben wie:
            
                    ABC.DEF."
            
            erkannt. Der Aufrufer bekommt in diesem Fall den Fehler 85 zurueck.
            '''
            akt_index += 1

            '''
            Innere While-Schleife zum Einlesen des Strings.
            Laeuft bis zum Stringende oder bis zum naechsten - nicht maskierten - Anfuehrungszeichen.
            '''
            while ( ( akt_index < laenge_eingabe_string ) and ( aktuelles_zeichen != '"' ) ):
            
                '''
                Aktuelles Pruefzeichen
                Das aktuelle Zeichen wird aus der Eingabe am aktuellen Index herausgelesen. 
                '''
                aktuelles_zeichen = pEingabe[ akt_index ];

                '''
                Alle erlaubten Stringzeichen werden durchgelassen. 
                Falsche Zeichen erzeugen einen Fehler.
                '''

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

                    '''
                    Der Leseprozessindex muss nach der While-Schleife auf dem jetzt
                    gerade gueltigen Index stehen. 
                    
                    Da am Ende dieser inneren While-Schleife der Leseprozess um 
                    eine Position weiter gestellt wird, muss der Index hier um 
                    eine Position verringert werden.
                    
                    Die aeussere While-Schleife erhoeht den Leseprozessindex nochmals. 
                    '''
                    akt_index -= 1
            
                elif ( aktuelles_zeichen == '\\' ):
                    '''
                    Maskiertes Zeichen 
                    Der Leseprozess muss nach naechste Zeichen pruefen. 
                    Der Leseprozessindex wird um ein Zeichen weiter gestellt.
                    '''
                    akt_index += 1

                    '''
                    Pruefung: Stringende ?
                    '''
                    if ( akt_index == laenge_eingabe_string ):
                        return 83 # String: Escape-Zeichen nicht am Ende der Eingabe

                    '''
                    Zeichen nach dem Backslash lesen. 
                    Das Zeichen darf ein Backslash oder ein Anfuehrungszeichen sein. 
                    Alle anderen Zeichen fuehren zum Fehler 84.
                    '''
                    aktuelles_zeichen = pEingabe[ akt_index ];

                    if ( ( aktuelles_zeichen != '\\' ) and ( aktuelles_zeichen != '@' ) and ( aktuelles_zeichen != ' ' ) and ( aktuelles_zeichen != '\'' ) and ( aktuelles_zeichen != '"' ) ):
                        return 84 # String: Ungueltige Escape-Sequenz im String

                    '''
                    Vermeidung dass die While-Schleife fruehzeitig beendet wird. 
                    Im Falle dass ein Anfuehrungszeichen gefunden wurde, wuerde 
                    die While-Schleife zum String einlesen beendet werden. 
                    '''
                    aktuelles_zeichen = 'A'
          
                else:
                    
                    '''
                    Fehler 89
                    Dieser Fehler wird zurueckgegeben, wenn ein ungueltiges 
                    Zeichen im String vorhanden ist.
                    '''
                    return 89 # String: Ungueltiges Zeichen innerhalb Anfuehrungszeichen

                '''
                Der Leseprozessindex wird um eine Position weitergestellt.
                '''
                akt_index += 1

            '''
            Leerstring 
            Wird ein abschliessendes Leerzeichen gefunden, darf die Differenz zur
            letzten Position eines Anfuehrungszeichens nicht 1 sein.
            '''
            if ( ( akt_index - position_anf_zeichen_akt ) == 1 ):
                return 85 # String: Leerstring in Anfuehrungszeichen "", oder Start mit Leerzeichen am Ende der Eingabe

            '''
            Pruefung: abschliessendes Anfuehrungszeichen vorhanden ?
           
            Nach dem Ende der While-Schleife, muss die Variable "aktuelles_zeichen" ein 
            Anfuehrungszeichen beinhalten. 
           
            Wurde kein abschliessendes Anfuehrungszeichen gefunden? 
            '''
            if ( aktuelles_zeichen != '"' ):
                return 86 # String: kein abschliessendes Anfuehrungszeichen gefunden.

            '''
            Pruefung: Leseprozess am Stringende angelangt ? 
            '''
            if ( akt_index + 1 >= laenge_eingabe_string ):
                return 88 # String: Der String endet am Stringende (Vorzeitiges Ende der Eingabe)

            '''
            Gueltige Abschlusszeichenkombinationen pruefen
            '''
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

            '''
            Position des letzten Anfuehrungszeichens merken
            '''
            position_anf_zeichen_akt = akt_index

            '''
            Es wurde ein String im Local-Part der eMail-Adresse erkannt. 
            Die Variable "fkt_ergebnis_email_ok" wird auf 1 gesetzt.
            '''
            fkt_ergebnis_email_ok = 1

        elif ( aktuelles_zeichen == '(' ):
      
            '''
            While-Schleife 4 - Kommentare
            '''

            '''
            Kommentare sind am Anfang oder am Ende des Local-Parts erlaubt.
            Im Domain-Part sind keine Kommentare zugelassen
            '''
            if ( position_at_zeichen > 0 ):
            
                '''
                Kombination ".(" pruefen Domain-Part.
                '''
                if ( ( position_letzter_punkt > position_at_zeichen ) and ( ( akt_index - position_letzter_punkt ) == 1 ) ):
                    return 102 # Kommentar: Falsche Zeichenkombination ".(" im Domain Part
            
            else:
        
                '''
                Kombination ".(" pruefen Local Part
                
                Wird eine einleitende Klammer gefunden, darf der letzte Punkt nicht 
                vor der Klammer liegen. 
                
                Die Position des letzten Punktes muss groesser als 0 sein. Bei weglassen 
                dieser Pruefung, kommt es zu einem Seiteneffekt mit dem Initialwert 
                von -1 der Variablen fuer den letzten Punkt. 
                
                Liegt eine falsche Zeichenkombination vor, wird der Fehler 101 zurueckgegeben.
                '''
                if ( ( position_letzter_punkt > 0 ) and ( ( akt_index - position_letzter_punkt ) == 1 ) ):
                    return 101 # Kommentar: Falsche Zeichenkombination ".(" im Local Part

            '''
            Wurde schon ein Kommentar gelesen, darf kein zweiter Kommentar
            zugelassen werden. Es wird der Feler 99 zurueckgegeben.
            '''
            if ( position_kommentar_ende > 0 ):
                return 99 # Kommentar: kein zweiter Kommentar gueltig

            '''
            Innere While-Schleife
            In einer inneren While-Schleife wird die IP-Adresse geparst und 
            auf Gueltigkeit geprueft. Die innere While-Schleife laeuft bis
            zum Stringende der Eingabe.
            '''

            '''
            Befindet sich der Leseprozess nicht am Anfang der eMail-Adresse, 
            muss nach dem Abschlusszeichen das AT-Zeichen folgen. 
            
            Kommentart innerhalb des lokalen Parts sind nicht erlaubt. 
            '''
            knz_abschluss_mit_at_zeichen = ( akt_index > 0 )

            knz_abschluss_mit_at_zeichen = ( akt_index == email_local_part_gesamt_start ) == False

            if ( position_at_zeichen > 0 ):
        
                '''
                Wurde schon ein AT-Zeichen gelesen, darf der Kommentar nicht auf einem AT-Zeichen enden. 
                '''
                knz_abschluss_mit_at_zeichen = False

                '''
                Sind schon Zeichen nach dem AT-Zeichen gelesen worden, muss der 
                Kommentar am Stringende enden.
                
                Endet der Kommentar vor dem Stringende, steht der Kommentar mitten 
                im eMail-String und ist somit falsch.
                '''
                if ( ( akt_index - position_at_zeichen ) > 1 ):
                    knz_kommentar_abschluss_am_stringende = True

            position_kommentar_start = akt_index

            akt_index += 1

            aktuelles_zeichen = 'A'

            while ( ( akt_index < laenge_eingabe_string ) and ( aktuelles_zeichen != ')' ) ):
        
                '''
                Aktuelles Pruefzeichen
                Das aktuelle Zeichen wird aus der Eingabe am aktuellen Index herausgelesen. 
                '''
                aktuelles_zeichen = pEingabe[ akt_index ]

                '''
                Alle erlaubten Stringzeichen werden durchgelassen. 
                Falsche Zeichen erzeugen einen Fehler.
                '''

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

                    '''
                    Der Leseprozessindex muss nach der While-Schleife auf dem jetzt
                    gerade gueltigen Index stehen. 
                    
                    Am Ende dieser inneren While-Schleife wird der Leseprozess um 
                    eine Position weiter gestellt. Der Leseprozessindex wird zum 
                    Ausgleich hier um eine Position verringert.
                    
                    Die aeussere While-Schleife erhoeht schlussendlich den Leseprozess, 
                    damit dieser dann auf das Zeichen nach dem hier gefundenen 
                    Anfuehrungszeichen verarbeiten kann. 
                    '''
                    akt_index -= 1
          
                elif ( aktuelles_zeichen == '\\' ):

                    '''
                    Maskiertes Zeichen 
                    Der Leseprozess muss nach naechste Zeichen pruefen. 
                    Der Leseprozessindex wird um ein Zeichen weiter gestellt.
                    '''
                    akt_index += 1

                    '''
                    Pruefung: Stringende ?
                    '''
                    if ( akt_index == laenge_eingabe_string ):
                        return 96 # Kommentar: Escape-Zeichen nicht am Ende der Eingabe

                    '''
                    Zeichen nach dem Backslash lesen. 
                    Das Zeichen darf ein Backslash oder ein Anfuehrungszeichen sein. 
                    Alle anderen Zeichen fuehren zum Fehler 91.
                    '''
                    aktuelles_zeichen = pEingabe[ akt_index ]

                    if ( ( aktuelles_zeichen != '\\' ) and ( aktuelles_zeichen != '"' ) ):
                        return 91 # Kommentar: Ungueltige Escape-Sequenz im Kommentar

                else:
                    
                    '''
                    Fehler 92
                    Dieser Fehler wird zurueckgegeben, wenn ein ungueltiges 
                    Zeichen im Kommentar vorhanden ist.
                    '''
                    return 92 # Kommentar: Ungueltiges Zeichen im Kommentar

                '''
                Der Leseprozessindex wird um eine Position weitergestellt.
                '''
                akt_index += 1

            '''
            Pruefung: Wurde eine abschliessende Klammer gefunden ? 
            
            Nach der While-Schleife muss die Variablen "aktuelles_zeichen" eine 
            abschliessende Klammer sein. Nur dann wurde die Einleseschleife 
            korrekt beendet. 
            
            Steht ein anderes Zeichen in der Variablen, ist der Leseprozess 
            am Stringende der Eingabe angekommen. Das ist die zweite Moeglichkeit, 
            wie die While-Schleife beendet werden kann. 
            '''
            if ( aktuelles_zeichen != ')' ):
                return 93 # Kommentar: kein abschliessendes Zeichen fuer den Komentar gefunden. ')' erwartet

            '''
            Pruefung: Leseprozess am Stringende angelangt ?
            
            Wurde die While-Schleife korrekt beendet, kann es sein, dass die 
            abschliessende Klammer am Stringende steht.  
            '''
            if ( akt_index + 1 >= laenge_eingabe_string ):

                if ( position_at_zeichen > 0 ):
                    ()
                    '''
                    Im Domain-Part darf der Kommentar am Stringende aufhoeren
                    '''
                else:
                    return 95 # Kommentar: Der Kommentar endet am Stringende (Vorzeitiges Ende der Eingabe)
        
            else:
                '''
                Pruefung: naechstes Zeichen gleich AT-Zeichen ?
                '''
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

            '''
            Die Position der abschliessenden Klammer wird gespeichert. 
            '''
            position_kommentar_ende = akt_index

            '''
            Leerzeichen nach Kommentar ----------------------------------------------------------------------
            
            Nach dem Kommentar koennen noch weitere Leerzeichen bis zur eMail-Adresse folgen.
            Diese Leerzeichen werden mittels einer While-Schleife ueberlesen.
            
                "(spaces after comment)     name1.name2@domain1.tld"
            '''
            if ( ( akt_index + 1 < laenge_eingabe_string ) and ( position_at_zeichen <= 0 ) ):

                if ( pEingabe[ akt_index + 1 ] == ' ' ):
          
                    '''
                    aktuelles Zeichen konsumieren, bzw. Lespositon 1 weiterstellen
                    '''
                    akt_index += 1

                    '''
                    Ueberlese alle Leerzeichen in einer While-Schleife. 
                    '''
                    while ( ( akt_index < laenge_eingabe_string ) and ( pEingabe[ akt_index ] == ' ' ) ):
                    
                        akt_index += 1
            
                    '''
                    Am Schleifenende wird die Leseposition erhoeht. 
                    Es wurde in dieser Bedingung fuer das Ueberlesen von Leerzeichen, der 
                    aktuelle Index um eine Position zu weit erhoeht. Dass muss korrigiert 
                    werden. Daher wird der aktuelle Index um 1 vermindert.
                    '''
                    akt_index -= 1
        
            '''
            Leerzeichen nach Kommentar ----------------------------------------------------------------------
            '''
 
        else:
            '''
            Sonderbedingung: Leerzeichentrennung bis Kommentar im Domain-Part
            
            "email@domain.com (joe Smith)"
            
            Ist das aktuelle Zeichen ein Leerzeichen und der Leseprozess befindet 
            sich im Domainpart (position_at_zeichen > 0), dann muss geprueft werden, 
            ob nach den Leerzeichen eine oeffnende Klammer kommt.
            '''
            if ( ( aktuelles_zeichen == ' ' ) and ( position_at_zeichen > 0 ) ):
            
                '''
                aktuelles Zeichen konsumieren, bzw. Lespositon 1 weiterstellen
                '''
                akt_index += 1

                '''
                Ueberlese alle Leerzeichen in einer While-Schleife. 
                '''
                while ( ( akt_index < laenge_eingabe_string ) and ( pEingabe[akt_index ] == ' ' ) ):
                    akt_index += 1

                '''
                Wurde in der While-Schleife bis zum Eingabeende gelesen, 
                wird der Fehler 22 zurueckgegeben, da das Leerzeichen 
                falsch ist.
                '''
                if ( akt_index == laenge_eingabe_string ):
                    return 22

                '''
                Nach der While-Schleife muss das Zeichen an der aktuellen 
                Leseposition eine oeffnende Klammer sein. Alle anderen 
                Zeichen fuehren zu einem Fehler, da das einleitende
                Leerzeichen ein falsches Zeichen war. Es wird in diesem 
                Fall der Fehler 105 zurueckgegeben. 
                '''
                if ( pEingabe[akt_index ] == '[' ):
                    # return 106 # Kommentar: Leerzeichentrennung im Domain-Part. 

                    akt_index -= 1
                    
                elif ( pEingabe[akt_index ] != '(' ):
                    return 105 # Kommentar: Leerzeichentrennung im Domain-Part. Oeffnende Klammer erwartet
                
                else:
                    '''
                    In der While-Schleife wurde die Leseposition einmal zu viel erhoeht.
                    Die Leseposition wird um eine Position verringert.
                    Da sich der Leseprozess im Domain-Part befindet gibt es ein vorhergehendes Zeichen.
                    '''
                    akt_index -= 1
            else:

                return 22 # Zeichen: ungueltiges Zeichen in der Eingabe gefunden
        
        akt_index += 1

    '''
    Pruefungen nach der While-Schleife    
    '''

    '''
    Pruefung: Punkt gefunden ?
    Bei einer IP-Adressangabe OK, da auch dort Punkte gefunden werden muessen.
    Bei einer IP6-Adressangabe wird die Variable "position_letzter_punkt" fuer 
    die Doppelpunkte ":" in der Adressangabe benutzt. 
    '''
    if ( ( position_letzter_punkt == -1 ) or ( position_letzter_punkt == position_at_zeichen ) ):
        return 34 # Trennzeichen: keinen Punkt gefunden (Es muss mindestens ein Punkt fuer den Domain-Trenner vorhanden sein)

    '''
    Pruefung: AT-Zeichen gefunden ?
    Ist der Wert der Variablen "position_at_zeichen" gleich -1, wurde kein AT-Zeichen 
    gefunden. Es wird der Fehler 28 zurueckgegeben.
      
    Bei einer IP-Adressangabe OK, da auch dort ein AT-Zeichen vorhanden sein muss.
    '''
    if ( position_at_zeichen == -1 ):
        return 28 # AT-Zeichen: kein AT-Zeichen gefunden

    '''
    Pruefung: EMail-Adresse ohne IP-Adressangabe ?
    
    Handelt es sich um eine eMail-Adresse ohne IP-Adresse, ist der Wert in der 
    Variablen "fkt_ergebnis_email_ok" kleiner als 2. 
    
    Wenn dem so ist, muessen noch Abschlusspruefungen bezueglich des letzten 
    Punktes gemacht werden.
    '''
    if ( fkt_ergebnis_email_ok < 2 ):
        '''
        Pruefung: Letzter Punkt nach AT-Zeichen ?
        Die Position des letzten Punktes muss groesser sein als die Position 
        des AT-Zeichens. Ist die Punkt-Position kleiner als die Position des 
        AT-Zeichens wird der Fehler 35 zurueckgegeben.

        Bei einer IP-Adressangabe OK, da dort die gleichen Bedingungen gelten.
        '''
        if ( position_letzter_punkt < position_at_zeichen ):
            return 35 # Trennzeichen: der letzte Punkt muss nach dem AT-Zeichen liegen (... hier eben die negative Form, wenn der letzte Punkt vor dem AT-Zeichen stand ist es ein Fehler)

        '''
        Pruefung: Letzter Punkt gleich Stringende ?
        Die Position des letzten Punktes darf nicht am Stringende liegen. 
        Liegt der letzte Punkt am Stringende, wird der Fehler 36 zurueckgegeben.

        Bei einer IP-Adressangabe OK, da dort die gleichen Bedingungen gelten.
        '''
        if ( ( position_letzter_punkt + 1 ) == laenge_eingabe_string ):
            return 36 # Trennzeichen: der letzte Punkt darf nicht am Ende liegen

        laenge_tld = 0

        if ( ( position_letzter_punkt > position_at_zeichen ) and ( position_kommentar_start > position_letzter_punkt ) ):
            #laenge_tld = position_kommentar_start - position_letzter_punkt;
            laenge_tld = 2 # pEingabe.substring( position_letzter_punkt, position_kommentar_start ).trim().length()
      
        else:
            laenge_tld = laenge_eingabe_string - ( position_letzter_punkt + 1 )

        '''
        https://stackoverflow.com/questions/15537384/email-address-validation-of-top-level-domain
        '''
        if ( laenge_tld < 2 ):
            return 14 # Laenge: Top-Level-Domain muss mindestens 2 Stellen lang sein.

        '''
        https://stackoverflow.com/questions/9238640/how-long-can-a-tld-possibly-be/9239264
        '''
        if ( laenge_tld > 63 ):
            return 15 # Laenge: Top-Level-Domain darf nicht mehr als 63-Stellen lang sein.

        '''
        https://stackoverflow.com/questions/9071279/number-in-the-top-level-domain
        '''

        aktuelles_zeichen = pEingabe[ position_letzter_punkt + 1 ]

        if ( ( aktuelles_zeichen >= '0' ) and ( aktuelles_zeichen <= '9' ) ):
            return 23 # Zeichen: Top-Level-Domain darf nicht mit Zahl beginnen

        # if ( zahlen_zaehler > 0 ) { return 19; } // Laenge: Top-Level-Domain darf keine Zahlen haben ... oder doch ?

    return fkt_ergebnis_email_ok

# Funktion assertIsTrue
def assertIsTrue( pInput=''):
    
    knz_is_valid_email_adress = validateEmail( pInput )
    
    if ( knz_is_valid_email_adress < 10 ):
        print(f'assertIsTrue  OK {knz_is_valid_email_adress} "{pInput}" ')
    else:
        print(f'assertIsTrue  #### Fehler {knz_is_valid_email_adress} #### "{pInput}" ')
        
def assertIsFalse(  pInput=''):
    
    knz_is_valid_email_adress = validateEmail( pInput )
    
    if ( knz_is_valid_email_adress >= 10 ):
        print(f'assertIsFalse OK {knz_is_valid_email_adress} "{pInput}" ')
    else:
        print(f'assertIsFalse #### Fehler {knz_is_valid_email_adress} #### "{pInput}" ')
        
def wlHeadline( pString = '' ):
    print( '' )
    print( f"---- {pString} ---------------------------------------------")
    print( '' )
        
wlHeadline( "Correct" )

assertIsTrue( "n@d.td" )
assertIsTrue( "1@2.td" )
assertIsTrue( "12.345@678.90.tld" )

assertIsTrue( "name1.name2@domain1.tld" )
assertIsTrue( "name1+name2@domain1.tld" )
assertIsTrue( "name1-name2@domain1.tld" )
assertIsTrue( "name1.name2@subdomain1.domain1.tld" )
assertIsTrue( "name1.name2@subdomain1.tu-domain1.tld" )
assertIsTrue( "name1.name2@subdomain1.tu_domain1.tld" )

assertIsTrue( "escaped.at\\@.sign@domain.tld" )
assertIsTrue( "\"at.sign.@\".in.string@domain.tld" )

assertIsTrue( "ip4.adress@[1.2.3.4]" )
assertIsTrue( "ip6.adress@[IPv6:1:2:3:4:5:6:7:8]" )
assertIsTrue( "ip4.embedded.in.ip6@[IPv6::ffff:127.0.0.1]" )
assertIsTrue( "ip4.without.brackets@1.2.3.4" )

assertIsTrue( "\"string1\".name1@domain1.tld" )
assertIsTrue( "name1.\"string1\"@domain1.tld" )
assertIsTrue( "name1.\"string1\".name2@domain1.tld" )
assertIsTrue( "name1.\"string1\".name2@subdomain1.domain1.tld" )
assertIsTrue( "\"string1\".\"quote2\".name1@domain1.tld" )
assertIsTrue( "\"string1\"@domain1.tld" )
assertIsTrue( "\"string1\\\"embedded string\\\"\"@domain1.tld" )
assertIsTrue( "\"string1(embedded comment)\"@domain1.tld" )

assertIsTrue( "(comment1)name1@domain1.tld" )
assertIsTrue( "(comment1)-name1@domain1.tld" )
assertIsTrue( "name1(comment1)@domain1.tld" )
assertIsTrue( "name1@(comment1)domain1.tld" )
assertIsTrue( "name1@domain1.tld(comment1)" )
assertIsTrue( "(spaces after comment)     name1.name2@domain1.tld" )
assertIsTrue( "name1.name2@domain1.tld   (spaces before comment)" )

assertIsTrue( "(comment1.\\\"comment2)name1@domain1.tld" )

assertIsTrue( "(comment1.\\\"String\\\")name1@domain1.tld" )
assertIsTrue( "(comment1.\\\"String\\\".@domain.tld)name1@domain1.tld" )

assertIsTrue( "(comment1)name1.ip4.adress@[1.2.3.4]" )
assertIsTrue( "name1.ip4.adress(comment1)@[1.2.3.4]" )
assertIsTrue( "name1.ip4.adress@(comment1)[1.2.3.4]" )
assertIsTrue( "name1.ip4.adress@[1.2.3.4](comment1)" )

assertIsTrue( "(comment1)\"string1\".name1@domain1.tld" )
assertIsTrue( "(comment1)name1.\"string1\"@domain1.tld" )
assertIsTrue( "name1.\"string1\"(comment1)@domain1.tld" )
assertIsTrue( "\"string1\".name1(comment1)@domain1.tld" )
assertIsTrue( "name1.\"string1\"@(comment1)domain1.tld" )
assertIsTrue( "\"string1\".name1@domain1.tld(comment1)" )

assertIsTrue( "<name1.name2@domain1.tld>" )
assertIsTrue( "name3 <name1.name2@domain1.tld>" )
assertIsTrue( "<name1.name2@domain1.tld> name3" )
assertIsTrue( "\"name3 name4\" <name1.name2@domain1.tld>" )

assertIsTrue( "name1 <ip4.adress@[1.2.3.4]>" )
assertIsTrue( "name1 <ip6.adress@[IPv6:1:2:3:4:5:6:7:8]>" )
assertIsTrue( "<ip4.adress@[1.2.3.4]> name1" )
assertIsTrue( "<ip6.adress@[IPv6:1:2:3:4:5:6:7:8]> name 1" )

assertIsTrue( "\"display name\" <(comment)local.part@domain-name.top_level_domain>" )
assertIsTrue( "\"display name\" <local.part@(comment)domain-name.top_level_domain>" )
assertIsTrue( "\"display name\" <(comment) local.part.\"string1\"@domain-name.top_level_domain>" )

assertIsTrue( "\"display name \\\"string\\\" \" <(comment)local.part@domain-name.top_level_domain>" )
assertIsTrue( "\"display name \\\"string\\\" \" <(comment)local.part.wiht.escaped.at\\@.sign@domain-name.top_level_domain>" )

assertIsTrue( "name1\\@domain1.tld.name1@domain1.tld" )
assertIsTrue( "\"name1\\@domain1.tld\".name1@domain1.tld" )
assertIsTrue( "\"name1\\@domain1.tld \\\"name1\\@domain1.tld\\\"\".name1@domain1.tld" )
assertIsTrue( "\"name1\\@domain1.tld \\\"name1\\@domain1.tld\\\"\".name1@domain1.tld (name1@domain1.tld)" )
assertIsTrue( "(name1@domain1.tld) name1@domain1.tld" )
assertIsTrue( "(name1@domain1.tld) \"name1\\@domain1.tld\".name1@domain1.tld" ) 
assertIsTrue( "(name1@domain1.tld) name1.\"name1\\@domain1.tld\"@domain1.tld" )

wlHeadline( "AT-Sign" )

assertIsFalse( "1234567890" )
assertIsFalse( "OnlyTextNoDotNoAt" )
assertIsFalse( "email.with.no.at.sign" )
assertIsFalse( "email.with.no.domain@" )
assertIsFalse( "@@domain.com" )

assertIsFalse( "name1.@domain.com" )
assertIsFalse( "name1@.domain.com" )
assertIsFalse( "@name1.at.domain.com" )
assertIsFalse( "name1.at.domain.com@" )
assertIsFalse( "name1@name2@domain.com" )

assertIsFalse( "email.with.no.domain\\@domain.com" )
assertIsFalse( "email.with.no.domain\\@.domain.com" )
assertIsFalse( "email.with.no.domain\\@123domain.com" )
assertIsFalse( "email.with.no.domain\\@_domain.com" )
assertIsFalse( "email.with.no.domain\\@-domain.com" )
assertIsFalse( "email.with.double\\@no.domain\\@domain.com" )
assertIsTrue( "\"wrong.at.sign.combination.in.string1@.\"@domain.com" )
assertIsTrue( "\"wrong.at.sign.combination.in.string2.@\"@domain.com" )

assertIsTrue( "email.with.escaped.at\\@.sign.version1@domain.com" )
assertIsTrue( "email.with.escaped.\\@.sign.version2@domain.com" )
assertIsTrue( "email.with.escaped.at\\@123.sign.version3@domain.com" )
assertIsTrue( "email.with.escaped.\\@123.sign.version4@domain.com" )
assertIsTrue( "email.with.escaped.at\\@-.sign.version5@domain.com" )
assertIsTrue( "email.with.escaped.\\@-.sign.version6@domain.com" )
assertIsTrue( "email.with.escaped.at.sign.\\@@domain.com" )

assertIsTrue( "(@) email.with.at.sign.in.commet1@domain.com" )
assertIsTrue( "email.with.at.sign.in.commet2@domain.com (@)" )
assertIsTrue( "email.with.at.sign.in.commet3@domain.com (.@)" )

assertIsFalse( "@@email.with.unescaped.at.sign.as.local.part" )
assertIsTrue( "\\@@email.with.escaped.at.sign.as.local.part" )
assertIsFalse( "@.local.part.starts.with.at@domain.com" )
assertIsFalse( "@no.local.part.com" )
assertIsFalse( "@@@@@@only.multiple.at.signs.in.local.part.com" )

assertIsFalse( "local.part.with.two.@at.signs@domain.com" )
assertIsFalse( "local.part.ends.with.at.sign@@domain.com" )
assertIsFalse( "local.part.with.at.sign.before@.point@domain.com" )
assertIsFalse( "local.part.with.at.sign.after.@point@domain.com" )
assertIsFalse( "local.part.with.double.at@@test@domain.com" )
assertIsTrue( "(comment @) local.part.with.at.sign.in.comment@domain.com" )
assertIsTrue( "domain.part.with.comment.with.at@(comment with @)domain.com" )
assertIsFalse( "domain.part.with.comment.with.qouted.at@(comment with \\@)domain.com" )
assertIsTrue( "\"String@\".local.part.with.at.sign.in.string@domain.com" )
assertIsTrue( "\\@.\\@.\\@.\\@.\\@.\\@@domain.com" )
assertIsFalse( "\\@.\\@.\\@.\\@.\\@.\\@@at.sub\\@domain.com" )
assertIsFalse( "@.@.@.@.@.@@domain.com" )
assertIsFalse( "@.@.@." )
assertIsFalse( "\\@.\\@@\\@.\\@" )
assertIsFalse( "@" )
assertIsFalse( "name @ <pointy.brackets1.with.at.sign.in.display.name@domain.com>" )
assertIsFalse( "<pointy.brackets2.with.at.sign.in.display.name@domain.com> name @" )
assertIsTrue( "<pointy.brackets3.with.escaped.at.sign.in.display.name@domain.com> name \\@" )

wlHeadline( "Seperator" )

assertIsFalse( "EmailAdressWith@NoDots" )

assertIsFalse( "..local.part.starts.with.dot@domain.com" )
assertIsFalse( "local.part.ends.with.dot.@domain.com" )
assertIsTrue( "local.part.with.dot.character@domain.com" )
assertIsFalse( "local.part.with.dot.before..point@domain.com" )
assertIsFalse( "local.part.with.dot.after..point@domain.com" )
assertIsFalse( "local.part.with.double.dot..test@domain.com" )
assertIsTrue( "(comment .) local.part.with.dot.in.comment@domain.com" )
assertIsTrue( "\"string.\".local.part.with.dot.in.String@domain.com" )
assertIsFalse( "\"string\\.\".local.part.with.escaped.dot.in.String@domain.com" )
assertIsFalse( ".@local.part.only.dot.domain.com" )
assertIsFalse( "......@local.part.only.consecutive.dot.domain.com" )
assertIsFalse( "...........@dot.domain.com" )
assertIsFalse( "name . <pointy.brackets1.with.dot.in.display.name@domain.com>" )
assertIsFalse( "<pointy.brackets2.with.dot.in.display.name@domain.com> name ." )

assertIsTrue( "domain.part@with.dot.com" )
assertIsFalse( "domain.part@.with.dot.at.domain.start.com" )
assertIsFalse( "domain.part@with.dot.at.domain.end1..com" )
assertIsFalse( "domain.part@with.dot.at.domain.end2.com." )
assertIsFalse( "domain.part@with.dot.before..point.com" )
assertIsFalse( "domain.part@with.dot.after..point.com" )
assertIsFalse( "domain.part@with.consecutive.dot..test.com" )
assertIsTrue( "domain.part.with.dot.in.comment@(comment .)domain.com" )
assertIsFalse( "domain.part.only.dot@..com" )
assertIsFalse( "top.level.domain.only@dot.." )

assertIsFalse( "...local.part.starts.with.double.dot@domain.com" )
assertIsFalse( "local.part.ends.with.double.dot..@domain.com" )
assertIsFalse( "local.part.with.double.dot..character@domain.com" )
assertIsFalse( "local.part.with.double.dot.before...point@domain.com" )
assertIsFalse( "local.part.with.double.dot.after...point@domain.com" )
assertIsFalse( "local.part.with.double.double.dot....test@domain.com" )
assertIsTrue( "(comment ..) local.part.with.double.dot.in.comment@domain.com" )
assertIsTrue( "\"string..\".local.part.with.double.dot.in.String@domain.com" )
assertIsFalse( "\"string\\..\".local.part.with.escaped.double.dot.in.String@domain.com" )
assertIsFalse( "..@local.part.only.double.dot.domain.com" )
assertIsFalse( "............@local.part.only.consecutive.double.dot.domain.com" )
assertIsFalse( ".................@double.dot.domain.com" )
assertIsFalse( "name .. <pointy.brackets1.with.double.dot.in.display.name@domain.com>" )
assertIsFalse( "<pointy.brackets2.with.double.dot.in.display.name@domain.com> name .." )

assertIsFalse( "domain.part@with..double.dot.com" )
assertIsFalse( "domain.part@..with.double.dot.at.domain.start.com" )
assertIsFalse( "domain.part@with.double.dot.at.domain.end1...com" )
assertIsFalse( "domain.part@with.double.dot.at.domain.end2.com.." )
assertIsFalse( "domain.part@with.double.dot.before...point.com" )
assertIsFalse( "domain.part@with.double.dot.after...point.com" )
assertIsFalse( "domain.part@with.consecutive.double.dot....test.com" )
assertIsTrue( "domain.part.with.comment.with.double.dot@(comment ..)domain.com" )
assertIsFalse( "domain.part.only.double.dot@...com" )
assertIsFalse( "top.level.domain.only@double.dot..." )

wlHeadline( "unsorted" )

assertIsTrue( 'name1@domain.com' )    
assertIsFalse( '' )
assertIsFalse( 'n@d.c')
assertIsFalse('name1.@domain.com')
assertIsFalse('name1@.domain.com')
assertIsFalse('@name1.at.domain.com')
assertIsFalse('name1.at.domain.com@')
assertIsFalse('name1@name2@domain.com')
assertIsFalse( 'name1.domain.com' )    

assertIsFalse( '.name1@domain.com' )    
assertIsFalse( 'name1.@domain.com' )    
assertIsFalse( 'name1@.domain.com' )    
assertIsFalse( 'name1@domain.com.' )    
assertIsFalse( 'name1..name2@domain.com' )    
assertIsFalse( 'name1@domain..com' )    

assertIsTrue( "&localandpart&with&$@amp.com" )
assertIsTrue( "*local**part*with*@asterisk.com" )
assertIsTrue( "$local$$part$with$@dollar.com" )
assertIsTrue( "=local==part=with=@equality.com" )
assertIsTrue( "!local!!part!with!@exclamation.com" )
assertIsTrue( "`local``part`with`@grave-accent.com" )
assertIsTrue( "#local##part#with#@hash.com" )
assertIsTrue( "-local--part-with-@hypen.com" )
assertIsTrue( "|localorpart|with|@pipe.com" )
assertIsTrue( "+local++part+with+@plus.com" )
assertIsTrue( "?local??part?with?@question.com" )
assertIsTrue( "~local~~part~with~@tilde.com" )
assertIsTrue( "^local^^part^with^@xor.com" )
assertIsTrue( "_local__part_with_@underscore.com" )
assertIsFalse( ":local::part:with:@colon.com" )

assertIsFalse( "local.part@&domainandpart&with&.com" )
assertIsFalse( "local.part@*domain**part*with*.com" )
assertIsFalse( "local.part@$domain$$part$with$.com" )
assertIsFalse( "local.part@=domain==part=with=.com" )
assertIsFalse( "local.part@!domain!!part!with!.com" )
assertIsFalse( "local.part@`domain``part`with`.com" )
assertIsFalse( "local.part@#domain##part#with#.com" )
assertIsFalse( "local.part@-domain--part-with-.com" )
assertIsFalse( "local.part@|domainorpart|with|.com" )
assertIsFalse( "local.part@+domain++part+with+.com" )
assertIsFalse( "local.part@?domain??part?with?.com" )
assertIsFalse( "local.part@~domain~~part~with~.com" )
assertIsFalse( "local.part@^domain^^part^with^.com" )
assertIsFalse( "local.part@_domain__part_with_.com" )

assertIsTrue( '"string1".name1@domain1.tld' )
assertIsTrue( "name1.\"string1\"@domain1.tld" )
assertIsTrue( "name1.\"string1\".name2@domain1.tld" )
assertIsTrue( "name1.\"string1\".name2@subdomain1.domain1.tld" )
assertIsTrue( "\"string1\".\"quote2\".name1@domain1.tld" )
assertIsTrue( "\"string1\"@domain1.tld" )
assertIsTrue( "\"string1\\\"embedded string\\\"\"@domain1.tld" )
assertIsTrue( "\"string1(embedded comment)\"@domain1.tld" )

assertIsTrue( "(comment1)name1@domain1.tld" )
assertIsTrue( "(comment1)-name1@domain1.tld" )
assertIsTrue( "name1(comment1)@domain1.tld" )
assertIsTrue( "name1@(comment1)domain1.tld" )
assertIsTrue( "name1@domain1.tld(comment1)" )
assertIsTrue( "(spaces after comment)     name1.name2@domain1.tld" )
assertIsTrue( "name1.name2@domain1.tld   (spaces before comment)" )


assertIsFalse( "email.with.no.domain\\@domain.com" )
assertIsFalse( "email.with.no.domain\\@.domain.com" )
assertIsFalse( "email.with.no.domain\\@123domain.com" )
assertIsFalse( "email.with.no.domain\\@_domain.com" )
assertIsFalse( "email.with.no.domain\\@-domain.com" )
assertIsFalse( "email.with.double\\@no.domain\\@domain.com" )
assertIsTrue( "\"wrong.at.sign.combination.in.string1@.\"@domain.com" )
assertIsTrue( "\"wrong.at.sign.combination.in.string2.@\"@domain.com" )

assertIsTrue( "email.with.escaped.at\\@.sign.version1@domain.com" )
assertIsTrue( "email.with.escaped.\\@.sign.version2@domain.com" )
assertIsTrue( "email.with.escaped.at\\@123.sign.version3@domain.com" )
assertIsTrue( "email.with.escaped.\\@123.sign.version4@domain.com" )
assertIsTrue( "email.with.escaped.at\\@-.sign.version5@domain.com" )
assertIsTrue( "email.with.escaped.\\@-.sign.version6@domain.com" )
assertIsTrue( "email.with.escaped.at.sign.\\@@domain.com" )

assertIsTrue( "(@) email.with.at.sign.in.commet1@domain.com" )
assertIsTrue( "email.with.at.sign.in.commet2@domain.com (@)" )
assertIsTrue( "email.with.at.sign.in.commet3@domain.com (.@)" )

