float rand(vec2 co) {
   return fract(sin(dot(co.xy, vec2(12.9898, 78.233))) * 43758.5453);
}

vec3 aplicar_grain(vec3 cor, vec2 uv, float time, float intensidade) {
   float ruido = rand(uv + fract(time)) - 0.5;
   return cor + ruido * intensidade;
}
