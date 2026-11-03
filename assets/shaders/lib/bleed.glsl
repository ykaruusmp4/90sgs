vec3 aplicar_bleed(sampler2D t, vec3 cor, vec2 uv, vec2 texel, float intensidade) {
   float r = texture(t, uv + vec2(texel.x * 1.5, 0.0)).r;
   return vec3(mix(cor.r, r, intensidade), cor.g, cor.b);
}
