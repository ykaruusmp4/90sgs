vec2 apply_glitch(vec2 uv, float time, float intensidade) {
   if (intensidade <= 0.0) return uv;

   float bloco = floor(uv.y * 15.0);
   float ruido = fract(sin(bloco + time * 10.0) * 43758.5453);

   if (ruido < intensidade * 0.8) {
      uv.x += (ruido - 0.5) * 0.15 * intensidade;
      uv.y += (ruido - 0.5) * 0.05 * intensidade;
   }
   return uv;
}
