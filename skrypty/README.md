Popugraf - wykres liczy ludności zamieszkującej obszar w danej odległości od inwestycji liniowej w funkcji jej długości.
W skrypcie oprócz plików wejściowych i wyjściowych należy ustawić wielkość bufora, odległość pomiędzy buforami, i liczbę ludzi którzy pokazani są jako otoczka o rozwarciu 1km.

Do posprzątania kwestie związane z układami współrzędnych.

Aktualnie działa wyłącznie z mapką gęstości zaludnienia Eurostatu według siatki kilometrowej (dostępne w folderze warstwy).
Sposób na przygotowanie linii kolejowej z OpenStreetMaps:
1) Szukamy linii kolejowej na OSM - wciskamy znak zapytania na jedną z nich, patrzymy na atrybut name i kopiujemy go
2) W QGIS używamy wtyczki QuickOSM, w QuickQuery szukamy według key: name i value <to co skopiowaliśmy z OSM>, klikamy advanced i zaznaczamy tylko Relation i Line
3) W tabeli atrybutów kasaujemy wszystkie kolumny oprócz pierwszej i zaznaczamy wszystkie wersje
4) Używamy wtyczki join multiple lines, w tabeli atrybutów widzimy tylko jedne pole. O to chodzi, tylko jednolitą linię możemy podzielić na równoodlełge punkty.

W skrypcie oprócz plików wejściowych i wyjściowych należy ustawić wielkość bufora, odległość pomiędzy buforami, i liczbę ludzi którzy pokazani są jako otoczka o rozwarciu 1km.