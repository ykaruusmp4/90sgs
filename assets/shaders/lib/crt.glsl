float hash21(vec2 p) {
   p = fract(p * vec2(123.34, 456.21));
   p += dot(p, p + 45.32);
   return fract(p.x * p.y);
}

vec2 crt_curvar(vec2 uv, float k) {
   vec2 c = uv * 2.0 - 1.0;
   c *= 1.0 + (c.yx * c.yx) * k;
   return c * 0.5 + 0.5;
}

float crt_mascara_borda(vec2 uv) {
   vec2 dist_borda = min(uv, 1.0 - uv);
   return smoothstep(0.0, 0.012, min(dist_borda.x, dist_borda.y));
}

vec3 crt_glow(sampler2D t, vec2 uv, vec2 texel) {
   vec3 glow = vec3(0.0);
   glow += texture(t, uv + vec2(texel.x, 0.0)).rgb;
   glow += texture(t, uv + vec2(-texel.x, 0.0)).rgb;
   glow += texture(t, uv + vec2(0.0, texel.y)).rgb;
   glow += texture(t, uv + vec2(0.0, -texel.y)).rgb;
   glow *= 0.25;
   return max(glow - 0.35, 0.0) * 0.45;
}

float crt_scanline(vec2 uv, float altura_res, float crt) {
   float sub = fract(uv.y * altura_res);
   float scan = 0.86 + 0.14 * sin(sub * 3.14159265);
   return mix(1.0, scan * 1.07, crt);
}

float crt_vinheta(vec2 uv, float crt) {
   float vig = uv.x * uv.y * (1.0 - uv.x) * (1.0 - uv.y) * 16.0;
   return pow(clamp(vig, 0.0, 1.0), mix(0.30, 0.45, crt));
}

vec3 crt_grao_flicker(vec3 cor, vec2 uv, vec2 res, float time, float crt) {
   float grao = hash21(floor(uv * res) + floor(time * 24.0)) - 0.5;
   cor += grao * 0.035 * crt;
   cor *= 1.0 + 0.012 * sin(time * 9.0) * crt;
   return cor;
}
