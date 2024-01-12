Per quanto riguarda il punto 3:
 - il field jobType delle sorgenti permette di categorizzare il traffico tramite un intero (1 = high, 0 = low)
 - tutti i pacchetti, quindi, emessi da src_high saranno taggati con type = 1, mentre quelli di src_low con type = 0
 - a questo punto il traffico viene inviato ai rispettivi server, che ignoreranno (ma preserveranno) questo tag
 - i server, ora, non sono collegati al sink, ma ad un classifier, che analizzera' il tag "type" succitato
 - dai docs del classifier:  
                "Sends the messages to different outputs depending on messages type or priority.
                If no output found for a message, it is sent to the "rest" gate.
                Messages with type = i will be sent to out[i] (if dispatchField = type).
                Messages with priority = i will be sent to out[i] (if dispatchField = priority)."
 - nel file ned si mette classifier.dispatcherField = 1;
 - in altre parole, il classifier mandera' tutti i messaggi con type = 1 all'uscita "out", mentre tutti gli altri all'uscita "rest"
 - per questo motivo, mettiamo l'uscita "out" collegata al sink "high" (ovvero quello che raccoglie i dati riguardanti il server_high), mentre rest al sink "low"