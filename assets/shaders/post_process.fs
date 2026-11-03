#version 330

#include "lib/crt.glsl"
#include "lib/dither.glsl"
#include "lib/aberracao.glsl"
#include "lib/perigo.glsl"
#include "lib/vignette.glsl"
#include "lib/glitch.glsl"
#include "lib/grain.glsl"
#include "lib/bleed.glsl"

uniform sampler2D tex;
uniform vec2 u_res;
uniform float u_time;
uniform float u_crt;
uniform float u_aberracao;
uniform float u_perigo;
uniform float u_dither;
uniform float u_glitch;

in vec2 v_texcoord;
out vec4 fragColor;

void main() {
   vec2 uv = v_texcoord;
   vec2 texel = 1.0 / u_res;

   uv = apply_glitch(uv, u_time, u_glitch);

   if (u_crt > 0.5) {
      uv = crt_curvar(uv, 0.02);
   }

   float forca_ab = aberracao_forca(u_aberracao, u_crt);
   vec3 col = amostrar_aberracao(tex, uv, texel, forca_ab);

   if (u_crt > 0.5) {
      col = aplicar_bleed(tex, col, uv, texel, 0.04);
   }

   if (u_crt > 0.5) {
      col += crt_glow(tex, uv, texel);
   }

   float vig = crt_vinheta(uv, u_crt);

   col = aplicar_perigo(col, vig, u_perigo, u_time);

   if (u_crt > 0.5) {
      col *= crt_scanline(uv, u_res.y, u_crt);
   }

   col = aplicar_grain(col, uv, u_time, 0.08);

   col *= vig;

   if (u_crt > 0.5) {
      col *= crt_mascara_borda(uv);
   }

   if (u_dither > 0.5) {
      col = aplicar_dither(col, uv, u_res, 16.0, u_dither);
   }

   fragColor = vec4(col, 1.0);
}
