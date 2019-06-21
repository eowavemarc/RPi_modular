# Utiliser Pure data
Pour faire tourner un patch Pd avec notre système, stocker-le dans un dossier dans la racine de votre clef usb.<br/> Nommez-le <b>main.pd</b> et joignez-y un fichier de configuration nommé <b>conf.txt</b>.<br/>
Vous trouverez dans ce dossier des objets utiles pour adapter un patch Pd à la plate-forme, pensez à les copier dans votre dossier. Toutes les informations necessaires sont à l'intérieur des objets en question.<br/>
# norme du fichier conf.txt
le système ne tient pas compte des espaces, tabulations et sauts de lignes, vous pouvez donc mettre en page ce fichier comme bon vous semble.<br/>
les caractères <b>=</b> séparent les déclarations et leur type. le fichier doit donc suivre la forme suivante :<br/>
<code><type de la première déclaration> = <première déclaration> = <type de la seconde déclaration> = <seconde déclaration></code> et ainsi de suite<br/>
les caractères <b>;</b> séparent les différents élements d'une déclaration.<br/>
<code><type de déclaration> = <premier élement de la déclaration> ; <second élément></code> etc.<br/>
les différents éléments sont automatiquement répartient sur les différentes pages de l'affichage en respectant l'ordre décrit dans <b>conf.txt</b>. Pour plus de détail, voir les exemples.
