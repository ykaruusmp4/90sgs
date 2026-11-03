float aberracao_forca(float aberracao, float crt) {
   return (1.5 + 4.5 * aberracao) * crt;
}

vec3 amostrar_aberracao(sampler2D t, vec2 uv, vec2 texel, float forca_px) {
   vec2 offset = (uv - 0.5) * forca_px * texel;
   vec3 cor;
   cor.r = texture(t, uv + offset).r;
   cor.g = texture(t, uv).g;
   cor.b = texture(t, uv - offset).b;
   return cor;
}
