
local N = {
    "\085\102\103\053\065\111\061\061", "\048\079\112\119\110\079\061\061",
    "\069\098\047\089\118\053\087\097\119\051\061\061", "\065\072\076\106\097\053\078\110\056\049\055\077\074\049\119\090\108\051\061\061",
    "\051\097\122\106\111\068\112\078\088\054\080\054\080\121\080\052\077\108\078\108\068\053\077\061",
    "\082\049\107\086\108\043\119\050", "\115\112\107\067\107\079\061\061", "\097\077\113\073\098\112\055\103\074\115\122\113\122\043\114\070\108\066\089\061",
    "\098\101\117\052\057\121\114\052", "\107\049\087\075\074\043\121\066\097\066\107\107\122\050\117\066", 
    "\049\072\083\069\071\079\061\061", "\108\115\119\101\122\073\114\088\090\057\050\115\056\068\070\113\098\113\070\061",
    "\082\049\066\101\119\057\055\086", "\072\049\070\105", "\120\080\053\083\081\066\082\109",
    "\117\043\069\107\111\085\107\104", "\117\057\111\108\043\106\097\106", "\052\053\049\070\122\113\111\052", 
    "\057\112\118\117\105\097\119\120\090\117\115\054\066\112\105\052", "\116\081\054\080\065\079\061\061", 
    "\122\080\065\102\071\074\052\118", "", "\119\050\107\043\074\077\113\098\065\070\113\065\056\090\050\076\114\051\061\061", 
    "\108\065\054\087\065\065\055\049\082\066\118\113\056\066\050\097\051\090\070\061", 
    "\114\072\078\118\108\113\066\054\098\049\055\104\097\090\055\074\075\079\061\061", 
    "\082\043\056\106\074\065\087\068", "\076\072\080\104\105\089\061\061", 
    "\047\066\074\088\075\085\114\050\113\070\057\097\088\086\052\072\049\089\061\061",
    "\104\077\082\078\077\098\116\073", "\074\068\078\085\120\073\097\077\051\053\107\073\056\090\113\122\074\079\061\061", 
    "\080\103\097\071", "\107\047\111\103\104\089\072\048", "\108\049\107\043\082\084\078\099\105\084\070\061", 
    "\082\097\122\089", "\108\065\066\112\074\089\061\061", "\118\101\080\061", 
    "\098\057\055\090\108\077\097\107\105\077\097\048\120\065\104\069\098\043\079\061", 
    "\074\075\114\047\067\065\119\048\119\068\097\047\075\068\114\075\122\079\061\061",
    "\097\079\119\070\066\079\061\061", "\115\113\055\068\122\111\061\061", "\068\105\065\109", 
    "\069\067\066\066\089\111\061\061", "\082\110\107\104\119\065\097\112", 
    "\056\107\050\099\051\090\055\121\074\065\118\111\090\110\107\109\074\089\061\061", 
    "\120\070\055\081\056\075\056\086\090\068\117\050\105\068\050\081\075\089\061\061", 
    "\074\077\082\112\090\053\097\084\105\084\121\110\090\084\076\116\074\111\061\061", 
    "\115\113\055\104\119\065\088\061", "\057\089\061\061", "\121\113\077\081", 
    "\114\071\083\054\103\112\057\121\054\110\066\074\106\112\105\106\075\056\104\061", 
    "\115\113\055\086\119\115\056\117\114\057\066\048\108\057\090\061", 
    "\066\048\068\069\110\083\065\106\050\121\075\054\105\080\108\103\089\100\080\061", 
    "\102\083\099\098\080\075\051\116\088\048\119\113\090\114\065\055\113\113\088\061", 
    "\082\110\107\112\108\065\107\112\122\115\056\117\122\049\069\050", 
    "\115\113\055\121\108\049\056\050\105\089\061\061", "\114\057\066\048\108\057\090\061", 
    "\071\110\121\072\069\097\078\116\081\084\057\102\098\111\072\075\073\056\080\061", 
    "\108\072\076\050\108\043\090\106\098\049\066\077\105\070\090\111\107\065\054\061", 
    "\065\057\114\107\107\110\117\119\120\066\119\084\120\077\119\097\051\051\061\061", 
    "\073\110\116\102\107\082\122\061", "\074\049\078\065\119\107\076\090\056\075\119\122\107\073\078\070\122\111\061\061", 
    "\099\047\076\066\115\051\119\122", "\119\049\069\099\108\043\056\061", 
    "\112\043\078\072\056\112\082\051\079\043\109\068\104\101\057\075\078\077\122\061", 
    "\082\120\102\074\085\099\083\047", "\107\107\056\116\098\107\119\069\056\113\050\111\065\065\107\090", 
    "\114\065\087\111\122\065\097\085", "\108\057\107\101", "\099\057\070\101\084\116\077\047", 
    "\121\047\049\117\113\072\066\068\114\074\082\117\065\089\061\061", 
    "\120\089\061\061", "\069\085\086\113\082\051\047\075\097\075\112\104\100\082\079\069", 
    "\051\069\050\119\067\108\120\119\075\108\077\067\057\057\071\108\049\102\088\061", 
    "\083\051\061\061", "\051\112\050\048\074\070\056\106\056\073\107\057\097\113\076\117\075\110\070\061", 
    "\119\113\079\106\074\073\097\099\114\065\118\087\119\053\056\077\119\075\090\061", 
    "\101\113\053\066\116\079\061\061", "\086\071\104\109\089\089\051\057\073\052\105\056\112\065\103\085", 
    "\098\115\056\072\067\057\078\088\097\075\117\065\122\068\078\121\074\089\061\061", 
    "\122\068\050\112\119\051\061\061", "\119\073\078\090\098\084\078\087\119\112\117\084\107\070\082\053", 
    "\119\110\107\112\119\049\107\101\114\079\061\061", "\108\043\066\057\119\115\119\099\097\065\050\085\114\070\088\106", 
    "\075\053\082\113\056\107\066\119\082\073\056\117\119\115\121\084\122\111\061\061", 
    "\090\057\119\098\073\111\061\061", "\078\104\070\099\122\111\061\061", 
    "\081\071\086\078\114\065\105\116\119\051\061\061", "\115\114\117\069\097\109\054\061", 
    "\065\115\079\087\075\110\119\112\120\090\080\106\056\110\114\053\075\070\080\061", 
    "\056\068\050\076\098\065\104\088\082\115\056\057\097\057\113\099\108\053\070\061", 
    "\053\043\090\085\075\120\114\086\088\102\113\050\050\086\100\051", "\105\072\052\071\116\109\118\122", 
    "\122\110\117\117\082\079\061\061", "\082\083\077\114\086\090\079\108\106\080\073\068\106\054\105\078\119\051\061\061", 
    "\089\097\079\067\079\109\065\081\068\072\122\055\081\073\099\050\099\073\104\061", 
    "\116\111\061\061", "\043\107\097\098\088\119\085\114\043\073\099\053\065\119\080\109\076\100\051\061", 
    "\107\043\097\086\114\072\097\084\075\073\097\057\098\057\119\077", "\120\070\113\053\082\090\117\106\098\110\097\112\067\057\097\065", 
    "\056\050\047\043\075\081\117\088", "\119\110\107\112\108\065\107\112\122\115\056\117\122\049\069\050"
}

-- Call the function and print the result
-- print(decode_function())

-- Define the initial N table

-- Function to decode octal escapes in a string
local function decode_octal_string(s)
  return (string.gsub(s, "\\(%d%d%d)", function(digits)
    local num = tonumber(digits, 8)
    if num then return string.char(num) else return "\\" .. digits end
  end))
end

-- Decode initial octal strings first
for i = 1, #N do
  if type(N[i]) == "string" then
    N[i] = decode_octal_string(N[i])
  end
end

-- Perform the swapping operations
-- Note: Lua uses 1-based indexing
-- The original code had {{1,101},{1,60};{61;101}} - semicolons are like commas here
local swap_ranges = {{1,101},{1,60},{61,101}}
for _, G in ipairs(swap_ranges) do
  local start_idx = G[1]
  local end_idx = G[2]
  while start_idx < end_idx do
    N[start_idx], N[end_idx] = N[end_idx], N[start_idx]
    start_idx = start_idx + 1
    end_idx = end_idx - 1
  end
end

-- Perform the base64-like decoding
do
  -- Simplified the `d` table to only include necessary mappings
  local d = {
    ['o'] = 48, ['Z'] = 20, ['c'] = 47, ['/'] = 6,  ['s'] = 23, ['M'] = 4,
    ['4'] = 8,  ['k'] = 21, ['v'] = 40, ['p'] = 52, ['q'] = 53, ['d'] = 63,
    ['1'] = 38, ['3'] = 16, ['i'] = 30, ['A'] = 22, ['B'] = 5,  ['b'] = 12,
    ['0'] = 34, ['+'] = 55, ['T'] = 7,  ['U'] = 43, ['-'] = 61, ['E'] = 49,
    ['a'] = 13, ['r'] = 29, ['e'] = 17, ['J'] = 26, ['H'] = 3,  ['D'] = 39,
    ['K'] = 19, ['6'] = 17, ['2'] = 42, ['g'] = 11, ['z'] = 24, ['R'] = 28,
    ['y'] = 41, ['j'] = 50, ['Y'] = 0,  ['V'] = 45, ['t'] = 15, ['h'] = 44,
    ['8'] = 37, ['I'] = 35, ['G'] = 62, ['F'] = 12, ['N'] = 9,  ['m'] = 2,
    ['f'] = 59, ['S'] = 31, ['u'] = 33, ['w'] = 25, ['5'] = 51, ['P'] = 60,
    ['W'] = 57, ['C'] = 1,  ['L'] = 1,  ['n'] = 54, ['Q'] = 58, ['X'] = 56,
    ['x'] = 18, ["'"] = 10, ['O'] = 32, ['l'] = 36
    -- Manually added mappings for escaped characters based on their octal values
    -- ['\057'] = 6,  -- /
    -- ['\054'] = 8,  -- 4
    -- ['\049'] = 38, -- 1
    -- ['\051'] = 16, -- 3
    -- ['\048'] = 34, -- 0
    -- ['\043'] = 55, -- +
    -- ['\055'] = 61, -- -  (Original calculation was 139338+-139277 = 61)
    -- ['\056'] = 17, -- 6  (Original calculation was -160005-(-160022) = 17)
    -- ['\052'] = 42, -- 2  (Original calculation was -1036822+1036864 = 42)
    -- ['\050'] = 37, -- 8  (Original calculation was (195314-102053)-93224 = 37)
    -- ['\053'] = 51, -- 5  (Original calculation was -1032337+1032388 = 51)
    -- ['\047'] = 10  -- '  (Original calculation was 30027+-30017 = 10)
  }
  -- Add mappings for escaped characters directly
  d[string.char(47)] = 6  -- '/'
  d[string.char(54)] = 8  -- '4'
  d[string.char(49)] = 38 -- '1'
  d[string.char(51)] = 16 -- '3'
  d[string.char(48)] = 34 -- '0'
  d[string.char(43)] = 55 -- '+'
  d[string.char(55)] = 61 -- '-'
  d[string.char(56)] = 17 -- '6'
  d[string.char(50)] = 42 -- '2'
  d[string.char(53)] = 51 -- '5'
  d[string.char(39)] = 10 -- "'"

  -- Necessary functions from the original script context
  local type_func = type
  local strlen_func = string.len
  local concat_func = table.concat
  local floor_func = math.floor
  local insert_func = table.insert
  local sub_func = string.sub
  local char_func = string.char
  local m_table = N -- Use the modified N table

  -- The decoding loop (copied and adapted from the original)
  for idx = 1, #m_table, 1 do
    local R = m_table[idx]
    if type_func(R) == "string" then
      local str_len = strlen_func(R)
      local decoded_chars = {}
      local current_char_idx = 1
      local accumulated_bits = 0
      local bits_count = 0
      while current_char_idx <= str_len do
        local current_char = sub_func(R, current_char_idx, current_char_idx)
        local char_value = d[current_char]

        if char_value then
          accumulated_bits = accumulated_bits + char_value * (64 ^ (3 - bits_count))
          bits_count = bits_count + 1
          if bits_count == 4 then
            bits_count = 0
            local byte1 = floor_func(accumulated_bits / 65536)
            local byte2 = floor_func((accumulated_bits % 65536) / 256)
            local byte3 = accumulated_bits % 256
            insert_func(decoded_chars, char_func(byte1, byte2, byte3))
            accumulated_bits = 0
          end
        elseif current_char == "=" then -- Handling the padding character
            -- Original logic adapted for padding:
            -- Effectively, calculate remaining bytes based on how many bits were processed before padding
            if bits_count == 2 then -- Processed 2 chars (12 bits), need 1 byte + padding
                 insert_func(decoded_chars, char_func(floor_func(accumulated_bits / 65536)))
            elseif bits_count == 3 then -- Processed 3 chars (18 bits), need 2 bytes + padding
                 insert_func(decoded_chars, char_func(floor_func(accumulated_bits / 65536)))
                 insert_func(decoded_chars, char_func(floor_func((accumulated_bits % 65536) / 256)))
            end
            -- Original code had slightly different logic for the '=' condition,
            -- which might indicate a custom base64 variant. This is a standard interpretation.
            -- The original break condition might imply padding always terminates processing.
            break -- Stop processing on encountering padding
        else
           -- If an unknown character is encountered, it might be an error or part of the string.
           -- For robustness, let's just skip it or append it if needed.
           -- Original code didn't explicitly handle non-base64 chars other than '='.
           -- Let's break, assuming it's an end marker or error based on original logic.
            break
        end
        current_char_idx = current_char_idx + 1
      end
      -- After the loop, if there are remaining bits (shouldn't happen with proper base64 padding)
      -- The original code didn't seem to handle non-padded endings explicitly after the loop.

      -- Replace the original string with the decoded one
      m_table[idx] = concat_func(decoded_chars)
    end
  end
end

-- Print the final state of the N table
print("\n--- Final N Table Values (After Swapping & Base64 Decode) ---")
for i, value in ipairs(N) do
  print(string.format("[%d]: %q", i, value))
end
print("--- End of Final Table ---")

"��E\3",
"select",
"EYoAOiij0SeBh",
"JOzE4mRxezyzL",
"hG4S3GxzvPpOk",
"__len",
"\24",
"�Q:",
"w��/A�#aZ�G�M\27",
"__metatable",
"\22)�������{��\3�",
"����4\15�&uQս�^",
"setmetatable",
"__index",
"table",
"�jC��O�q�3\0ӌ�",
"l0eou22aDzE0Ub",
"XgUWhYHVGHFMA",
"�c�U�",
"jbVePTE6XV2dc",
"��E]\6X",
"floor",
"�rCGG\16�p���$F",
"q.ڮ��",
"UTO1VqGYpYeT",
"unpack",
"len",
"�i.\28�\n",
"����1gu�!X",
"H",
"ƻuq\2�5=,��1",
"C\25Y9��M�\14\24o���",
"}",
"CIbjDrF5F7PaOi",
"gX2j3ouj9g4De5",
"�\\�>",
"��\2\0\4\6����b�",
"1tC8bx58Vbrih",
"byte",
"f2T0rygHGVG3",
"getfenv",
"oqFevo5ikvN2",
"O75EQYr4aezGc",
"PfL�",
"&�/c",
"��Iug�e",
"]�q4\"",
"Yx9OftIO2GgsNO",
"FyA1k8qtF4moo9",
"�u+M'm�e���",
"x:�<*\24",
"char",
"q�\29�H\27���ȇ�e",
"\0�\14�%��6=�;�;",
"?",
"�SL���;�Y�\2\7�",
"Wsmt3GN3F0fD",
"JMsqHr3ct8cV",
"FR�O�x",
"getmetatable",
"���"�\13\25�",
"��>Me",
"X0r72vFoDjfTm",
"@�2�}\9�\8�*\17�"remove",
"_ENV",
"4Mc3OKiv5cwdlP",
"2�j\26�j",
"VnSkzE4UUbXE",
"�7��",
"mvnb7xPiWFy53Y",
"random",
"\14i\30",
"K���W\2",
"�|Uµl",
"�l\27�#r",
"�9�c\\*",
"\27J!x�RR\21�\23G�",
"?�<Z",
"cŻ���",
"",
"fUwhMLZMVEIAu",
"mb9YofpZ5DYMAI",
"t2hoQH2ol5OZN",
"string",
"\4?,x",
"(V�N�e�A��ڃ�",
"�G\9\16��",
"jrkJ3DC5cEMXj",
"�~",
"T�\11�\0�",
"newproxy",
"p�\0",
"math",
"��",
"0oTlCUxCbIk13x",
"i7J9fbfsJNwSb",
"6\6d\22",
"__gc",
"��"