const float bayer4x4[16] = float[16](
      0.0, 0.5, 0.125, 0.625,
      0.75, 0.25, 0.875, 0.375,
      0.1875, 0.6875, 0.0625, 0.5625,
      0.9375, 0.4375, 0.8125, 0.3125
   );

vec3 aplicar_dither(vec3 cor, vec2 uv, vec2 res, float niveis, float intensidade) {
   ivec2 vp = ivec2(floor(uv * res));
   int idx = (vp.x & 3) + (vp.y & 3) * 4;
   float limiar = bayer4x4[idx] - 0.5;
   float passos = niveis - 1.0;
   return floor(cor * passos + 0.5 + limiar * intensidade) / passos;
}
