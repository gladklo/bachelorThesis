Allgemeine Dinge zu Beachten von ihm:



Glasklar was von mir ist und was nicht der Arbeit

Teams egal

teams und SAP ist nicht die welt und aus forschungssicht irrelevant

Im Rahmen mussten wir uns auf Teams / Copilot ... beschränken (limitation) aber es ist eben ein reales arbeitssetting

&#x09;Warum ist es die bestmögliche Umgebung (literatur) -> Es gibt keine ready Anwendungen die das Kombinieren oder Möglichkeiten einfach auf SAP Systeme zuzugreifen oder das deployment zu Teams ermöglichen



Schwerpunkt ist die Auswertung

KI muss sagen könne was sie kann und was nicht nach nutzeranfrage





1 Mail (18.02.2026)-----------------------------------------------------------------------------



1\. Darf ich digital Abgeben?



Soweit ich weiß ja, bitte in Moodle hochladen und zusätzlich an beide Betreuer per Mail mit dem informellen Hinweis im Mailtext, dass es sich bei dem PDF um eine identische Version zur finalen Abgabe in Moodle handelt. Trotzdem der Disclaimer: Keine Garantie bei meinen Antworten zu formalen Prüfungsabläufen, im Zweifel noch mal beim Prüfungsamt oder dem Studiengangsleiter fragen.



6\. Muss ich nichtfunktionale anforderungen definieren und beschreiben, selbst wenn diese theoretisch nicht relevant sind? (Geht ja in der Arbeit um den Konkreten fall ob KI helfen kann, wenn eben alles funktioniert (best case)



Ähnlich zu Authentifizierung kann es interessant sein, das kurz zu beschreiben, aber eben in der gebotenen Kürze. Wenn Sie die bei Ihrer Arbeit aber gar nicht berücksichtigen, dann ist es egal, ich würde dann aber einen Disclaimer schreiben (Limitations, Grenzen der Arbeit), wo sie darauf eingehen, dass NFRs nicht berücksichtigt werden (vielleicht kann man da aber dann ein paar Beispiele für relevante NFRs geben, die man berücksichtigen könnte).



Viele Grüße,



Kai Eckert



2 Mail (01.03.2026)-----------------------------------------------------------------------------





1\. Literaturanalyse

&#x20;     1. Die Bachelorarbeit wird ca.40 Seiten lang (ohne Anhänge). Ist dieses Kapitel pauschal zu lang / kurz?



Kann man pauschal nicht sagen, insofern nein. Der Text wimmelt von Fehlern, das wird hoffentlich noch besser. Immer erst mal beschreiben, worum es im betrachteten Paper geht, der Einstieg mit der ersten Referenz ist da schon grenzwertig, da fehlt der Kontext. Kurz beschreiben, um was es geht und dann mit der eigenen Arbeit (und ggf. anderen) in Bezug setzen.



&#x20;     3. Am ende schließe ich den Bogen wie erwähnt zu meiner Arbeit und habe offene Fragen / "Probleme" festgestellt. Gehört sowas noch in die Literaturanalyse.



Ja, kann man machen. Normalerweise erwarte ich die Identifikation von Lücken eher in der Einleitung. Auf jeden Fall muss nicht nur eine Lücke identifiziert werden, sondern der eigene Ansatz sollte in Bezug zu anderen Arbeiten gesetzt werden. Ob man das alles in einem macht, ist dann eher Geschmackssache.





Viele Grüße,



Kai Eckert





3 Mail (03.03.2026)-----------------------------------------------------------------------------





2\. "der Einstieg mit der ersten Referenz ist da schon grenzwertig" Meinen Sie die Referenz im erstem Abschnitt (Kapitelreferenz) oder die erste Quelle?



Die erste Quelle. "WährendDesouza, Dawson und Chenok vor allem die praktischen Herausforde-

rungen der Implementierung solcher Systeme im öffentlichen Sektor hervorheben,"



!!!Was sind solche Systeme? Danach werden LLMs erwähnt, aber erst mal fehlt der Kontext!!!. Und welchen Bezug hat das zu Ihrer Arbeit? Das sind Kleinigkeiten, die leicht zu bereinigen sind, und wenn es nicht immer perfekt ist, ist das auch nicht so schlimm (daher grenzwertig). Aber gleich als erster Satz ist es ungeschickt, wenn man da gleich ins Stolpern kommt.



&#x09;	**LITERATURANALYSE UMSCHREIBEN**



4 Mail (31.03.2026)-----------------------------------------------------------------------------





>

> 1. Meine Implementierung besteht ja wie gesagt aus 2 Chatbots. Der Lösungsansatz war ja aber zu beginn eine Implementierung mit einem Chatbot der alles kann.

>     -> Soll im das Lösungsansatz Kapitel dann der Ansatz mit 1 oder 2 Bots beschrieben werden. Wobei in der "Implementierung" dann beschrieben wird warum es jetzt 2 sind.

>



Das ist ein bisschen Geschmacksache. Grundsätzlich sind Sie nicht an den Wortlaut Ihres Exposes oder der ursprünglichen Fragestellung gebunden. Natürlich sollten Sie grob beim Thema bleiben, aber die Arbeit schreiben Sie komplett aus Ihrem aktuellen Kenntnisstand heraus. Entsprechend können Sie von Anfang an Ihren Ansatz mit 2 Bot skizzieren, allerdings muss dann trotzdem klar werden, warum Sie hier zwei Bots benötigen. Alternativ können Sie das Problem allgemein formulieren und dann (wie von Ihnen vorgeschlagen) in der Umsetzung auf die Notwendigkeit des 2. Bots eingehen. Ich sehe das allerdings nicht bei der Implementierung, sondern bereits im Konzept Ihres konkreten Ansatzes, denn da müssen Sie ja schon anfangen, den 2. Bot einzuplanen.



Wirklich entscheidend ist am Ende eigentlich nur, dass sich von der Forschungsfrage über den von Ihnen (durchaus durch lokale Anforderungen und Gegebenheiten beeinflusst) gewählten Lösungsansatz bis zur Bewertung der letztlich implementierten Lösung ein roter Faden ergibt, dem man argumentativ gut folgen kann.



&#x09;	**SO UMSETZTEN DAS IM LÖSUNGSANSATZKAPITEL GESAGT WIRD, DASS MEHRERE AGENTENERSTELLUNGSPLATTFORMEN GETESTET WERDEN -> DARAUS RESULTIERT, DASS COPILOT FÜR A UND JOULE FÜR B BENUTZT WIRD -> Dann Umsetzung Kapitel✅**





> 2. In der Checkliste steht, dass "die Darstellung der Implementierung knapp ausfallen kann". Ich habe bis jetzt erklärt wie ich die Tools benutzt habe und wie der Ablauf innerhalb von Joule Studio und Copilot Studio ist. (5 Seiten ink Abbildungen).

>     -> Soll ich noch zusätzlich auf Details, wie eine konkrete Erläuterung der Prompts und Beschreibungen der Tools (die der Chatbot zum fetchen der Daten verwendet) eingehen, oder reichen allgemeine Aussagen wie "die Datenbankfelder wurden in der Beschreibung des Tools welches die API Anfragen sendet beschrieben / dem Agenten wurde Aufgetragen die Antworten immer in einem Passendem Format wiederzugeben"



Liefern Sie für relevante Prompts Beispiele mit, so dass klar wird, wie Sie bei der Entwicklung vorgegangen sind. Weitere, bzw. normalerweise alle Prompttemplates gehören in den Anhang. Die Beispiele brauchen Sie, weil die Arbeit auch ohne Anhang verständlich sein soll. Der Anhang vervollständigt das ganze nur und zeigt, dass Sie mehr als nur ein paar Promptbeispiele gemacht haben.



&#x09;	**WENN ICH IN IMPLEMENTIERUNG ETWAS BEGRÜNDE SOLL EIN BEISPIEL PROMPT REIN UND DEMENTSPRECHEND DER TEIL DES SYSTEM PROMPTS**

&#x09;	**Alle Systemprompts in den Anhang (nochmal durchlesen) und in Implementierung in einer subsection\* auf besonderheiten in den Prompts eingehen**

>

> 3. Erwarten Sie in dem Ergebnis Teil zwingend Quellen? Wenn ich auf erarbeitete Usecases / Probleme oder Bereits Realisierte Unterstützungen durch den Chatbot eingehe, fällen mir wenig Punkte ein die ich in irgend einer weise mit Quellen belegen kann?

> Literatur habe ich in meiner Arbeit eigentlich im Kapitel eingebunden in dem ich das vorgehen in den Tests (Qualitätssicherung) beschreibe.

> Falls sie Literatur hier erwarten, hätten Sie ein konkretes Beispiel?

>



Ein wirklich passendes Beispiel müsste ich auch erst recherchieren und dafür bräuchte ich mehr Details zu Ihrer Arbeit. Was ich mir vorstellen kann, sind Paper, die in ähnlich gelagerten Szenarien z.B. bestimmte Stärken oder Schwächen von KI-Systemen gezeigt haben. Da wäre es interessant, ob Sie die in Ihren Ergebnissen bestätigen können. Wenn es da überhaupt nichts passendes gibt, dann ist das eben so. Allerdings sollte ich dann auch nicht sofort etwas finden, wenn ich danach suche, sobald ich Ihre Arbeit in der Hand habe. Natürlich wird es keine Arbeiten geben, die genau das machen, was Sie machen, aber doch sicherlich einige, die in einer ähnlichen Richtung unterwegs sind.



Hier ein paar Beispiele, aber keine Ahnung, wie gut die wirklich zu Ihrem Ansatz passen:



https://arxiv.org/abs/2412.12386

https://ieeexplore.ieee.org/abstract/document/11160657

https://aclanthology.org/2024.findings-naacl.284/

&#x09;

&#x09;	**EIN BISSCHEN NACH ARBEITEN MIT ÄHNLICHEN ERGEBNISSEN SUCHEN IN DEN EINZELNEN BLÖCKEN**



5 Mail (31.03.2026)-----------------------------------------------------------------------------



>

> Ich bin gerade dabei das "Lösungsansatz" Kapitel auszuformulieren in dem ich meine Lösung vorstelle.

>

> --> 1. Beim schreiben habe ich mich gefragt ob überhaupt konkrete Technologien wie Joule Studio / Microsoft Studio erwähnt werden sollen oder ich bei allgemeinen Begriffen wie "KI-Agent-Orchestrierungsplattformen" (oder was auch immer dafür genau der Name ist) bleiben soll? <--

>

> Also anstatt "Es wird Joule Studio verwendet weil es Funktionen wie Authentifizierung in MS Teams und Zugriff auf das oData backend bereit hat"

>

> schreibe ich "Um die Unterstützung wie in den Anforderungen beschrieben zu realisieren, soll der Chatbot mithilfe eines KI Agenten implementiert werden über dessen Skills die verschiedenen Funktionen umgesetzt werden"

>

> und dann in beiden fällen eben Alternativen, Begründung usw. und später dann im Implementierungskapitel Konkret: In Joule wurde X gemacht und in Copilot Y.

>

> Aus der Checkliste werde ich leider auch nicht schlau weil da das Level an Konkretheit nicht genannt wird.

>



Auf jeden Fall von Anfang an möglichst verständlich formulieren, nicht künstlich abstrakt schreiben. Ich würde unterscheiden zwischen allgemeinen Anforderungen, die sich aus der Problemstellung ergeben und konkreten Anforderungen, die sich aus dem firmeninternen Setup ergeben. Authentifizierung könnte man argumentieren, dass man die immer braucht, um einen persönlichen Kontext zu haben, aber selbst dann ist eben die eigentliche Anforderung ggf., dass mit einer persönlichen Historie gearbeitet werden soll oder einem Kontext-File für das LLM, das Informationen zu den letzten Sitzungen enthält.



Darüber kann sich dann die konkrete Anforderung ergeben, dass man das System in das vorhandene Authentifizierungssystem einbinden muss. Spätestens wenn Sie bei konkreten Microsoft-Produkten angekommen sind, ist das für die Fragestellung nicht mehr interessant, trotzdem gehört es in die Arbeit, um zu zeigen, wie die praktische Umsetzung in einem realen Setting aussieht.



Analog zur letzten Mail würde ich auch hier grob eine Dreiteilung sehen: **allgemeine Problemstellung und Lösungsansätze, Konzept für eine Umsetzung, und schließlich Beschreibung der konkreten Umsetzung in der Firma mit konkreten Softwareprodukten.**



&#x09;	**KONZEPT FÜR UMSETZUNG EINBINDEN🤔 reicht lösungsansatz nicht?**



\-> Muss ich direct zwischen allgemeinen Und Firmenanforderungen unterschieden? Also muss ich alles so explizit labeln oder reicht es indirect, wenn ich es tue ohne für alles eine exktra section / subsection zu gliedern?

\-> ES gibt keine Problemstellung

\-> Kann das konzept im Lösungsansatz sein? Ich verstehe das so bisschen als das Selbe. Ich sage im Lösungsansatz dass ich es mit "Agenterstellungsplattformen" versuche weil ..., und erwähne auch warum ich bestimmte alternativen nicht gewählt habe. Da ist ja das Konzept schon integriert so wie ich das verstehe? 







