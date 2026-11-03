vec3 apply_vignette(vec3 col, vec2 uv) {
   float d = length(uv - vec2(0.5));
   float vig = smoothstep(0.8, 0.3, d);
   return col * vig;
}
