' Supprime toutes les lignes qui contiennent un mot clef
Const ForReading = 1, ForWriting = 2, ForAppending = 8
Dim fso, f_in, f_out
mot_clef = "Ç"
Set fso = CreateObject("Scripting.FileSystemObject" )
Set f_in = fso.OpenTextFile("toto.txt", ForReading)
Set f_out = fso.OpenTextFile("toto_tmp.txt", ForWriting, true)
Do Until f_in.AtEndOfStream
   une_ligne = f_in.ReadLine
   token_pos = Instr(une_ligne, mot_clef)
   If (token_pos = 0) Then
	  ' Recopie la ligne si elle ne contient pas le mot clef
	  f_out.WriteLine une_ligne
   End If
Loop
f_in.Close
f_out.Close
' Remplace toto.txt par le nouveau fichier toto_tmp_.txt
fso.DeleteFile "toto.txt", true
fso.MoveFile "toto_tmp.txt", "toto.txt"