float aberracao_forca(float aberracao, float crt) {
   return (0.35 + 1.65 * aberracao) * crt;
}

vec3 amostrar_aberracao(sampler2D t, vec2 uv, vec2 texel, float forca) {
   float ab = forca * length(uv * 2.0 - 1.0);
   vec3 cor;
   cor.r = texture(t, uv + vec2(ab * texel.x, 0.0)).r;
   cor.g = texture(t, uv).g;
   cor.b = texture(t, uv - vec2(ab * texel.x, 0.0)).b;
   return cor;
}
