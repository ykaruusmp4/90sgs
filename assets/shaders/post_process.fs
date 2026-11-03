#version 330 core

in vec2 uvs;
out vec4 f_color;

uniform sampler2D tex;
uniform vec2 u_res;
uniform float u_time;
uniform float u_crt;
uniform float u_aberracao;
uniform float u_perigo;
uniform float u_dither;

const float NIVEIS = 8.0;
const float DITHER = 0.70;

#include "lib/crt.glsl"
#include "lib/aberracao.glsl"
#include "lib/perigo.glsl"
#include "lib/dither.glsl"

void main() {
   vec2 uv = crt_curvar(uvs, 0.045 * u_crt);

   if (uv.x < 0.0 || uv.x > 1.0 || uv.y < 0.0 || uv.y > 1.0) {
      f_color = vec4(0.0, 0.0, 0.0, 1.0);
      return;
   }

   float mascara = crt_mascara_borda(uv);
   vec2 texel = 1.0 / u_res;

   vec3 cor = amostrar_aberracao(tex, uv, texel, aberracao_forca(u_aberracao, u_crt));
   cor += crt_glow(tex, uv, texel) * u_crt;
   cor *= crt_scanline(uv, u_res.y, u_crt);

   float vig = crt_vinheta(uv, u_crt);
   cor *= vig;

   cor = aplicar_perigo(cor, vig, u_perigo, u_time);
   cor = crt_grao_flicker(cor, uv, u_res, u_time, u_crt);

   cor = pow(max(cor, vec3(0.0)), vec3(0.92));
   cor *= mix(1.0, mascara, u_crt);

   cor = mix(cor, aplicar_dither(cor, uv, u_res, NIVEIS, DITHER), u_dither);

   f_color = vec4(clamp(cor, 0.0, 1.0), 1.0);
}
