<template>
  <div>
    <div class="row">
      <div class="col-6">
        <card title="Descriptif" subTitle="">
          <p>Certains changements dans le règlement du hockey dans la NHL ont permis une rapide évolution du jeu
            dans cette ligue, beaucoup disent que le jeu a perdu en dimension physique mais gagné en vitesse et
            nombre de buts inscrits, est-ce vrai ?<br>
            Au cours d'une saison, on remarque une différence d'intensité
            drastique entre un match de saison régulière et un match de playoff, nous allons tenter de le démontrer.</p>
          <p>Ce site est composé de trois pages, cette page d'accueil, une page qui permet de démontrer l'évolution
            globale du hockey en NHL durant les 9 dernières saisons, et une page qui permet de comparer la saison
            régulière
            au playoff pour une saison particulière</p>
        </card>
      </div>
      <div class="col-6">
        <card title="Source des données" subTitle="">
          Toutes les données utilisées sont issues d'un jeu de donnéee nommée NHL Game Data hébergée sur Kaggle:
          <br>
          <a href="https://www.kaggle.com/martinellis/nhl-game-data" target="_blank">source des données</a>
        </card>
      </div>
    </div>
  </div>
</template>

<script>
  export default {
    name: "About"
  }
</script>

<style scoped>

</style>
