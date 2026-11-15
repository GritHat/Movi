# MoVi — diagrammi UML

I diagrammi sono scritti in Mermaid: GitHub li disegna da solo aprendo questo file. Descrivono il prototipo
simulato (`prototipo/`) e la dimostrazione 3D (`prototipo/unreal/`). MoVi osserva e avvisa: nessuna uscita è un
comando al veicolo.

## 1. Casi d'uso

Mermaid non ha un tipo «casi d'uso»: il diagramma usa gli attori ai lati e i casi d'uso come ovali.

```mermaid
flowchart LR
    op(["Operatore"])
    veic(["Veicolo senza equipaggio<br/>(sistema di bordo)"])
    sens(["Sensori<br/>radar, camera, infrarosso"])
    cls(["Classificatore<br/>(supposto esistente)"])
    mappa(["Mappa degli ostacoli"])

    subgraph MoVi
        uc1(("Seguire un oggetto<br/>in movimento"))
        uc2(("Dichiarare lo stato:<br/>visto, regione, non so"))
        uc3(("Mantenere la regione<br/>di un oggetto non visto"))
        uc4(("Stimare la confidenza<br/>nel tempo"))
        uc5(("Dichiarare un sensore<br/>non affidabile"))
        uc6(("Rilevare un evento<br/>improvviso"))
        uc7(("Avvisare di una<br/>possibile presenza"))
        uc8(("Dichiarare libero<br/>solo ciò che è osservato"))
        uc9(("Registrare e convalidare<br/>ogni ciclo"))
    end

    sens --> uc1
    sens --> uc5
    cls --> uc1
    mappa --> uc8
    uc1 --> uc2
    uc2 -. include .-> uc3
    uc3 -. include .-> uc4
    uc5 -. extend .-> uc6
    uc6 -. include .-> uc7
    uc3 -. include .-> uc7
    uc7 --> op
    uc7 --> veic
    uc2 --> op
    uc8 --> veic
    uc9 --> op
```

## 2. Componenti

```mermaid
flowchart LR
    subgraph Ingresso
        S1["Radar"]
        S2["Camera"]
        S3["Infrarosso"]
        ET["Etichette di classe<br/>(a mano nel prototipo)"]
        CF["Configurazione:<br/>scenario e portatore"]
    end
    subgraph Nucleo["Nucleo MoVi"]
        SA["Salute dei sensori"]
        FU["Fusione e associazione"]
        ST["Stimatore<br/>Kalman a più modelli"]
        RE["Regione e confidenza"]
        EV["Eventi e volume dei detriti"]
        MA["Mappa a stati"]
        AV["Avviso"]
    end
    subgraph Uscita
        RG["Registro per ciclo"]
        VI["Viste e filmato"]
        TB["Tabellone e convalida"]
    end
    S1 --> SA
    S2 --> SA
    S3 --> SA
    SA --> FU
    ET --> FU
    CF --> ST
    FU --> ST
    ST --> RE
    SA --> EV
    FU --> EV
    RE --> MA
    EV --> MA
    MA --> AV
    AV --> RG
    MA --> RG
    RG --> VI
    RG --> TB
```

## 3. Classi del nucleo

Le classi sono quelle di `prototipo/unreal/movi_core.py`, il porto compatto del nucleo usato nella dimostrazione 3D.

```mermaid
classDiagram
    class Asse {
        +float p
        +float v
        +float a
        +float b
        +float c
        +float q
        +float r
        +prevedi(dt)
        +aggiorna(z)
    }
    class Traccia {
        +Asse[] assi
        +float non_visto_da
        +str stato
        +passo(dt, misura)
        +pos
        +sigma
        +raggio90
        +confidenza(r_porta) float
    }
    class MoVi {
        +Traccia traccia
        +float r_porta
        +bool avviso
        +float t_avviso
        +bool evento
        +passo(t, dt, misura, radar_ok, camera_ok) dict
    }
    MoVi "1" *-- "1" Traccia : segue
    Traccia "1" *-- "3" Asse : un filtro per asse
```

`Asse` è un filtro di Kalman a velocità costante su un asse, con covarianza `[[a, b], [b, c]]`.
`Traccia.raggio90` è il raggio della regione al 90 %: 2,146 volte `sigma`.
`Traccia.confidenza` è C = 1 − exp(−r² / 2σ²).

## 4. Sequenza: collisione vicina con sensori accecati

Scenario della scorta: il drone che porta MoVi segue un bersaglio veloce; accanto, due droni collidono.

```mermaid
sequenceDiagram
    autonumber
    participant Sim as Scena simulata
    participant Sen as Sensori
    participant Sal as Salute dei sensori
    participant Sti as Stimatore
    participant Map as Mappa a stati
    participant Avv as Avviso
    participant Vei as Veicolo e operatore

    loop a ogni ciclo, bersaglio visibile
        Sim->>Sen: posizione vera del bersaglio
        Sen->>Sal: misura con rumore
        Sal->>Sti: misura valida
        Sti->>Map: posizione stimata, regione piccola
        Map->>Vei: stato «visto»
    end

    Sim->>Sen: collisione: lampo, fumo, detriti
    Sen->>Sal: camera satura, radar saturo
    Sal->>Avv: sensori non affidabili insieme
    Avv->>Vei: avviso immediato: evento vicino, posizione non nota

    loop mentre i sensori sono accecati
        Sal->>Sti: nessuna misura
        Sti->>Sti: sola previsione, la covarianza cresce
        Sti->>Map: regione più larga, confidenza più bassa
        Map->>Vei: stato «non visto: regione», mai «libero»
    end

    Sim->>Sen: il fumo si dirada
    Sen->>Sal: misura di nuovo valida
    Sal->>Sti: misura valida
    Sti->>Map: la regione si stringe sul bersaglio
    Map->>Vei: stato «visto», bersaglio ripreso
```

## 5. Stati di una traccia

```mermaid
stateDiagram-v2
    [*] --> Candidata : prima misura
    Candidata --> Visto : conferma su più cicli
    Candidata --> [*] : nessuna conferma
    Visto --> Visto : misura associata
    Visto --> NonVistoRegione : nessuna misura
    NonVistoRegione --> Visto : misura coerente con la regione
    NonVistoRegione --> NonVistoRegione : previsione, la regione cresce
    NonVistoRegione --> PrevistoAmpio : confidenza sotto la soglia
    PrevistoAmpio --> Visto : riacquisizione, identità «presunta»
    PrevistoAmpio --> NonSo : regione oltre il campo osservabile
    NonSo --> Visto : nuova traccia confermata
    NonSo --> [*] : tutta la zona guardata e vista libera

    Visto : Visto
    NonVistoRegione : Non visto, regione dichiarata
    PrevistoAmpio : Previsto ampio
    NonSo : Non so
```

## 6. Stati dell'avviso di possibile presenza

L'avviso non si spegne per tempo, identità o operatore: si spegne solo guardando tutta la zona.

```mermaid
stateDiagram-v2
    [*] --> Spento
    Spento --> Acceso : oggetto non più visto
    Spento --> Acceso : sensori accecati insieme
    Acceso --> Acceso : la zona non è tutta osservata
    Acceso --> Spento : tutta la zona osservata e libera
```

## 7. Stati di un sensore

```mermaid
stateDiagram-v2
    [*] --> Affidabile
    Affidabile --> NonAffidabile : saturazione, fumo, guasto
    NonAffidabile --> Affidabile : segnale valido per più cicli
    NonAffidabile --> NonAffidabile : dichiarato a ogni ciclo

    NonAffidabile : Non affidabile, dichiarato
```

## 8. Attività: un ciclo di percezione

```mermaid
flowchart TD
    A(["Inizio del ciclo"]) --> B["Leggi i sensori"]
    B --> C{"Sensore affidabile?"}
    C -- no --> D["Dichiara il sensore non affidabile"]
    C -- sì --> E["Associa le misure alle tracce"]
    D --> F{"Tutti i sensori accecati?"}
    F -- sì --> G["Avviso immediato: evento vicino"]
    F -- no --> E
    G --> H["Prevedi ogni traccia"]
    E --> H
    H --> I{"Misura per la traccia?"}
    I -- sì --> J["Aggiorna il filtro: stato «visto»"]
    I -- no --> K["Allarga la regione, abbassa la confidenza"]
    K --> L["Accendi l'avviso di possibile presenza"]
    J --> M["Aggiorna la mappa a stati"]
    L --> M
    M --> N{"Cella osservata e vuota?"}
    N -- sì --> O["Cella «libera»"]
    N -- no --> P["Cella «non osservata»: mai «libera»"]
    O --> Q["Scrivi il registro del ciclo"]
    P --> Q
    Q --> R(["Fine del ciclo"])
```
