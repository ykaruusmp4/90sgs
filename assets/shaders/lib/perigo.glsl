vec3 aplicar_perigo(vec3 cor, float vig, float perigo, float time) {
   float pulso = 0.5 + 0.5 * sin(time * 7.0);
   float borda = 1.0 - vig;
   vec3 vermelho = vec3(cor.r + 0.35, cor.g * 0.35, cor.b * 0.35);
   return mix(cor, vermelho, clamp(perigo * borda * (0.4 + 0.6 * pulso) * 1.6, 0.0, 1.0));
}
