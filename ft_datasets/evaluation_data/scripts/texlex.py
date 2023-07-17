import ply.lex as lex

# List of token names.   This is always required
tokens = (
    'NUM',
    'VAR',
    'ADD',
    'NEG',
    'TIMES',
    'DIV',
    'FRAC',
    'FRAC__',
    'ABOVE',
    '_OVER',
    'PRIME',
    'SUBSCRIPT',
    'SUPSCRIPT',
    'BINOM',
    'BINOM__',
    'CHOOSE',
    'SQRT',
    'ROOT',
    '_OF',
    'VECT',
    'MODULAR',
    'FACT',
    '_QVAR',
    'TAB_ROW',
    'TAB_COL',
    '_BEGIN_MAT',
    '_END_MAT',
    '_STACKREL',
    '_BUILDREL',
    '_SET_REL',
    'X_ARROW',
    '_L_BRACKET',
    '_L_DOT',
    '_L_ANGLE',
    '_L_SLASH',
    '_L_HAIR',
    '_L_BSLASH',
    '_L_ARROW',
    '_L_TEX_BRACE',
    '_L_TEX_BRACKET',
    '_R_BRACKET',
    '_R_DOT',
    '_R_ANGLE',
    '_R_SLASH',
    '_R_HAIR',
    '_R_ARROW',
    '_R_TEX_BRACE',
    '_R_TEX_BRACKET',
    '_L_CEIL',
    '_L_FLOOR',
    '_R_CEIL',
    '_R_FLOOR',
    'SUM_CLASS',
    'SEP_CLASS',
    'REL_CLASS',
    'FUN_CLASS',
    'ENV',
    'newline',
    '_L_VERT',
    '_R_VERT',
    'INFTY',
    '_SCRIPT',
    'SINGLE_LETTER',
    'STYLE'
)

t_NUM = r'\d+\.?\d*'

# t_ADD    = r"\+|±|\\oplus|\\uplus|\\dotplus|\\pm|\\mp"
# t_NEG   = r'-|\\neg|\\ominus|\\setminus|\\backslash|\\smallsetminus|\\lnot|\\barwedge'
# t_TIMES   = r'\\times|\\cdot|\\otimes|\\ltimes|\\rtimes|\\odot'
# t_DIV = r'/|\\div|\\divideontimes'
# t_ABOVE = r'\\above'
# t__OVER = r'\\over'
# t_PRIME = r'\'|\\prime'
# t_SUBSCRIPT = r'_'
# t_SUPSCRIPT = r'\^'
# t_BINOM = r'\\dbinom|\\tbinom|\\binom'
# t_BINOM__ =r'\\dbinom[ ]*[0-9][0-9]|\\tbinom[ ]*[0-9][0-9]|\\binom[ ]*[0-9][0-9]'
# t_CHOOSE = r'\\choose|\\brack'
# t_SQRT = r'\\sqrt'
# t_ROOT = r'\\root'
# t__OF = r'\\of'
# t_VECT = r'\\vec|\\overrightarrow|\\overleftarrow'
# t_MODULAR = r'\\pmod|\\bmod|\\mod|\\pod'
# t_FACT = '!'
# t__QVAR = r'\\qvar'
# t_TAB_ROW = r'\\\\|\\cr|\\newline'
# t_TAB_COL = '&'
# t__BEGIN_MAT = r'\\begin\{matrix\}|\\begin\{vmatrix\}|\\begin\{Vmatrix\}|\\begin\{bmatrix\}|\\begin\{Bmatrix\}|\\begin\{pmatrix\}|\\begin\{smallmatrix\}|\\begin\{cases\}|\\array\{'
# t__END_MAT = r'\\end\{matrix\}|\\end\{vmatrix\}|\\end\{Vmatrix\}|\\end\{bmatrix\}|\\end\{Bmatrix\}|\\end\{pmatrix\}|\\end\{smallmatrix\}|\\end\{cases\}'
# t__STACKREL = r'\\stackrel'
# t__BUILDREL = r'\\buildrel'
# t__SET_REL = r'\\overset|\\underset'
# t_X_ARROW = r'\\xleftarrow|\\xrightarrow'


# t__L_BSLASH =
#t__L_TEX_BRACE = r'\{'
#t__L_TEX_BRACKET = r'\['
#t__R_DOT = r'\\right[ ]*\.|\\right'
#t__R_ANGLE = r'\\right[ ]*\\rangle|\\rangle|\\right[ ]*>'
#t__R_SLASH = r'\\right[ ]*/|\\right[ ]*\\|\\right[ ]*\\backslash'
#t__R_HAIR = r'\\right[ ]*\\rmoustache|\\rmoustache'
#t__R_ARROW = r'\\right[ ]*\\[Uu]parrow|\\right[ ]*\\[Dd]ownarrow|\\right[ ]*\\[Uu]pdownarrow'
#t__R_BRACKET = r'\)|\\}|[\\right[ ]*]?\\rgroup|\\rbrace|\\rbrack|\\right[ ]*\}|\\right[ ]*\]|\\right[ ]*\)'
#t__R_TEX_BRACE = r'}'
#t__R_TEX_BRACKET = r']'

t__L_CEIL = r'[\\left[ ]*]?\\lceil'
t__L_FLOOR = r'[\\left[ ]*]?\\lfloor'
t__R_CEIL = r'[\\right[ ]*]?\\rceil'
t__R_FLOOR = r'[\\right[ ]*]?\\rfloor'

t_SINGLE_LETTER = r'[a-zA-Z]'
t_VAR = r'\*|\\ast|\\Alpha|\\Beta|\\Chi|\\Delta|\\Epsilon|\\Eta|\\Gamma|\\Iota|\\Kappa|\\Lambda|\\Mu|\\Nu|\\Omega|\\Omicron|\\Phi|\\Pi|\\Psi|\\Re|\\Rho|\\Sigma|\\Tau|\\Theta|\\Upsilon|\\VarLambda|\\VarOmega|\\Xi|\\Zeta|\\aleph|\\alpha|\\amalg|\\beta|\\beth|\\chi|\\delta|\\ell|\\epsilon|\\eta|\\eth|\\gamma|\\imath|\\iota|\\jmath|\\kappa|\\lambda|\\mho|\\mu|\\nu|\\omega|\\omicron|\\phi|\\psi|\\rho|\\sigma|\\tau|\\theta|\\top|\\upsilon|\\varDelta|\\varGamma|\\varPhi|\\varPi|\\varPsi|\\varSigma|\\varTheta|\\varUpsilon|\\varXi|\\varepsilon|\\varkappa|\\varphi|\\varpi|\\varpropto|\\varrho|\\varsigma|\\vartheta|\\wr|\\xi|\\zeta|\\backepsilon|\\partial|\\nabla|\\pi|\\empty|\\emptyset|\\emptyset|\\varnothing|\\triangledown|\\triangle|\\angle|\\vartriangleleft|\\vartriangleright|\\vartriangle|\\triangleleft|\\triangleright|\\measuredangle|\\sphericalangle|\\perp|\\bot|\\circ|\\%|\\.\\.\\.|\\dots|\\ldots|\\vdots|\\cdots|\\ddots|\\ddot|\\dddot|\\ddddot|\\dotsb|\\dotsc|\\dotsi|\\dotsm|\\dotso|\\iddots|\||\\\\\||\\vert|\\Vert|\\Arrowvert|\\arrowvert|\\bracevert|\\rvert|\\lvert|\\rVert|\\lVert|\\mid|\\nmid'
t_SEP_CLASS = r'\\exists|\\nexists|\\forall|\||\\cr|\\newline|\\\\|\\enspace|\\atop|,|;|\\colon|:|\\And|\\\\&|\\qquad|\\quad|\\to|\\searrow|\\uparrow|\\updownarrow|\\upharpoonleft|\\upharpoonright|\\upuparrows|\\Leftarrow|\\Leftrightarrow|\\Lleftarrow|\\Longleftarrow|\\Longleftrightarrow|\\Longrightarrow|\\Lsh|\\Rightarrow|\\Rrightarrow|\\Rsh|\\Uparrow|\\Updownarrow|\\circlearrowleft|\\circlearrowright|\\curvearrowleft|\\curvearrowright|\\Downarrow|\\downarrow|\\downdownarrows|\\downharpoonleft|\\downharpoonright|\\hookleftarrow|\\hookrightarrow|\\gets|\\iff|\\impliedby|\\implies|\\leftarrow|\\leftarrowtail|\\leftharpoondown|\\leftharpoonup|\\leftleftarrows|\\leftrightarrow|\\leftrightarrows|\\leftrightharpoons|\\leftrightsquigarrow|\\longleftarrow|\\longleftrightarrow|\\longmapsto|\\longrightarrow|\\looparrowleft|\\looparrowright|\\mapsto|\\multimap|\\nLeftarrow|\\nLeftrightarrow|\\nRightarrow|\\nearrow|\\nleftarrow|\\nleftrightarrow|\\nrightarrow|\\nwarrow|\\rightarrow|\\rightarrowtail|\\rightharpoondown|\\rightharpoonup|\\rightleftarrows|\\rightleftharpoons|\\rightrightarrows|\\rightsquigarrow|\\swarrow|\\leadsto'
t_FUN_CLASS = r'\\operatorname\*?\{[^}]*\}|\\exp|\\lg|\\ln|\\log|\\sin|\\sinh|\\arcsin|\\cos|\\arccos|\\cosh|\\tan|\\tanh|\\arctan|\\cot|\\coth|\\csc|\\sec|\\sgn|\\signum|\\sign|\\max|\\min|\\Pr|\\deg|\\det|\\dim|\\gcd|\\hom|\\ker'
#t_SUM_CLASS = r'\\arg|\\inf|\\sup|\\liminf|\\limsup|\\varliminf|\\varlimsup|\\bigcap|\\bigcup|\\bigsqcup|\\biguplus|\\bigvee|\\bigwedge|\\bigcirc|\\bigodot|\\bigoplus|\\bigotimes|\\bigtriangledown|\\bigtriangleup|\\sum|\\prod|\\coprod|\\lim|\\injlim|\\varinjlim|\\varprojlim|\\projlim|\\idotsint|\\int|\\iint|\\iiint|\\iiiint|\\intop|\\smallint|\\oint'
t_REL_CLASS = r'=|:=|\\[dD]oteq|\\dot=|\\approxeq|\\backsimeq|\\circeq|\\cong|\\backsim|\\curlyeqprec|\\curlyeqsucc|\\eqslantgtr|\\eqslantless|\\equiv|\\gnsim|\\triangleq|\\eqsim|\\thicksim|\\sim|\\simeq|\\nsim|\\neq|\\not(=|\\equiv)|\\frown|\\between|\\eqcirc|\\smallfrown|\\smallsmile|\\approx|\\asymp|\\ge|\\geq|\\geqq|\\geqslant|\\gg|\\gnapprox|\\gt|>|\\gtrapprox|\\gtrdot|\\gtreqless|\\gtreqqless|\\gtrless|\\gtrsim|\\le|\\leq|\\leqq|\\leqslant|\\lessapprox|\\lessdot|\\lesssim|\\ll|\\lnapprox|\\lneq|\\lneqq|\\lt|<|\\lvertneqq|\\ncong|\\ne|\\ngeq|\\ngeqq|\\ngeqslant|\\nleq|\\nleqq|\\nleqslant|\\nless|\\nprec|\\npreceq|\\nsucc|\\nsucceq|\\prec|\\preceq|\\succ|\\succapprox|\\succcurlyeq|\\thickapprox|\\trianglelefteq|\\trianglerighteq|\\succeq|\\succnapprox|\\succneqq|\\succnsim|\\succsim|\\unlhd|\\unrhd|\\gneq|\\gneqq|\\gvertneqq|\\ggg|\\gggtr|\\ngtr|\\precapprox|\\preccurlyeq|\\precnapprox|\\precneqq|\\precnsim|\\precsim|\\Cap|\\cap|\\Cup|\\cup|\\curlyvee|\\dashv|\\curlywedge|\\land|\\lor|\\sqcap|\\sqcup|\\vee|\\veebar|\\wedge|\\Join|\\bowtie|\\Subset|\\Supset|\\nsubseteq|\\nsupseteq|\\supseteq|\\subset|\\sqsubset|\\sqsubseteq|\\sqsupset|\\sqsupseteq|\\subseteq|\\subseteqq|\\subsetneq|\\subsetneqq|\\supset|\\supseteq|\\supseteqq|\\supsetneq|\\supsetneqq|\\varsubsetneq|\\varsubsetneqq|\\varsupsetneq|\\varsupsetneqq|\\in|\\ni|\\not\\in|\\owns|\\nparallel|\\parallel|\\propto'


def t_FRAC__(t):
    r'\\frac[ ]*[0-9][0-9]|\\dfrac[ ]*[0-9][0-9]|\\cfrac[ ]*[0-9][0-9]|\\tfrac[ ]*[0-9][0-9]'
    return t


def t_FRAC(t):
    r'\\frac|\\dfrac|\\cfrac|\\tfrac'
    return t


def t__L_ARROW(t):
    r'\\left[ ]*\\[Uu]parrow|\\left[ ]*\\[Dd]ownarrow|\\left[ ]*\\[Uu]pdownarrow'
    return t


def t__L_VERT(t):
    r'\\left[ ]*\|'
    return t


def t__R_VERT(t):
    r'\\right[ ]*\|'
    return t


def t__L_ANGLE(t):
    r'\\left[ ]*\\langle|\\langle|\\left[ ]*<'
    return t


def t__L_BRACKET(t):
    r'\(|\\{|[\\left[ ]*]?\\lgroup|\\lbrace|\\lbrack|\\left[ ]*\[|\\left[ ]*\{|\\left[ ]*\('
    return t


def t__L_SLASH(t):
    r'\\left[ ]*/|\\left[ ]*\\|\\left[ ]*\\backslash'
    return t


def t__L_HAIR(t):
    r'\\left[ ]*\\lmoustache|\\lmoustache'
    return t


def t__L_DOT(t):
    r'\\left[ ]*\.|\\left'
    return t


def t_ADD(t):
    r'\+|±|\\oplus|\\uplus|\\dotplus|\\pm|\\mp'
    return t


def t_NEG(t):
    r'-|\\neg|\\ominus|\\setminus|\\backslash|\\smallsetminus|\\lnot|\\barwedge'
    return t


def t_TIMES(t):
    r'\\times|\\cdot|\\otimes|\\ltimes|\\rtimes|\\odot'
    return t


def t_DIV(t):
    r'/|\\div|\\divideontimes'
    return t


def t_ABOVE(t):
    r'\\above'
    return t



def t_PRIME(t):
    r'\'|\\prime'
    return t


def t_SUBSCRIPT(t):
    r'_'
    return t


def t_SUPSCRIPT(t):
    r'\^'
    return t


def t_BINOM(t):
    r'\\dbinom|\\tbinom|\\binom'
    return t


def t_BINOM__(t):
    r'\\dbinom[ ]*[0-9][0-9]|\\tbinom[ ]*[0-9][0-9]|\\binom[ ]*[0-9][0-9]'
    return t


def t_CHOOSE(t):
    r'\\choose|\\brack'
    return t


def t_SQRT(t):
    r'\\sqrt'
    return t


def t_ROOT(t):
    r'\\root'
    return t


def t__OF(t):
    r'\\of'
    return t


def t_VECT(t):
    r'\\vec|\\overrightarrow|\\overleftarrow'
    return t


def t_MODULAR(t):
    r'\\pmod|\\bmod|\\mod|\\pod'
    return t


def t_FACT(t):
    '!'
    return t


def t__QVAR(t):
    r'\\qvar'
    return t


def t_TAB_ROW(t):
    r'\\\\|\\cr|\\newline'
    return t


def t_TAB_COL(t):
    '&'
    return t


def t__BEGIN_MAT(t):
    r'\\begin\{matrix\}|\\begin\{vmatrix\}|\\begin\{Vmatrix\}|\\begin\{bmatrix\}|\\begin\{Bmatrix\}|\\begin\{pmatrix\}|\\begin\{smallmatrix\}|\\begin\{cases\}|\\array\{'
    return t


def t__END_MAT(t):
    r'\\end\{matrix\}|\\end\{vmatrix\}|\\end\{Vmatrix\}|\\end\{bmatrix\}|\\end\{Bmatrix\}|\\end\{pmatrix\}|\\end\{smallmatrix\}|\\end\{cases\}'
    return t


def t__STACKREL(t):
    r'\\stackrel'
    return t


def t__BUILDREL(t):
    r'\\buildrel'
    return t


def t__SET_REL(t):
    r'\\overset|\\underset'
    return t


def t_X_ARROW(t):
    r'\\xleftarrow|\\xrightarrow'
    return t


def t_INFTY(t):
    r'\\infty|∞'
    return t
def t_SUM_CLASS(t):
    r'\\arg|\\inf|\\sup|\\liminf|\\limsup|\\varliminf|\\varlimsup|\\bigcap|\\bigcup|\\bigsqcup|\\biguplus|\\bigvee|\\bigwedge|\\bigcirc|\\bigodot|\\bigoplus|\\bigotimes|\\bigtriangledown|\\bigtriangleup|\\sum|\\prod|\\coprod|\\lim|\\injlim|\\varinjlim|\\varprojlim|\\projlim|\\idotsint|\\int|\\iint|\\iiint|\\iiiint|\\intop|\\smallint|\\oint'
    return t

def t__L_TEX_BRACE(t):
    r'\{'
    return t

def t__L_TEX_BRACKET(t):
    r'\['
    return t

def t__R_DOT(t):
    r'\\right[ ]*\.|\\right'
    return t

def t__R_ANGLE(t):
    r'\\right[ ]*\\rangle|\\rangle|\\right[ ]*>'
    return t

def t__R_SLASH(t):
    r'\\right[ ]*/|\\right[ ]*\\|\\right[ ]*\\backslash'
    return t

def t__R_HAIR(t):
    r'\\right[ ]*\\rmoustache|\\rmoustache'
    return t

def t__R_ARROW(t):
    r'\\right[ ]*\\[Uu]parrow|\\right[ ]*\\[Dd]ownarrow|\\right[ ]*\\[Uu]pdownarrow'
    return t

def t__R_BRACKET(t):
    r'\)|\\}|[\\right[ ]*]?\\rgroup|\\rbrace|\\rbrack|\\right[ ]*\}|\\right[ ]*\]|\\right[ ]*\)'
    return t

def t__R_TEX_BRACE(t):
    r'}'
    return t

def t__R_TEX_BRACKET(t):
    r']'
    return t

def t_STYLE(t):
    r'\\mathbb|\\overline|\\mathrm|\\underline|\\mathcal|\\mathbf|\\mathop|\\emph'
    return t

def t__OVER(t):
    r'\\over'
    return t

def t__ENV(t):
    r'\\begin\{align\}|\\end\{align\}|\\begin\{align\*\}|\\end\{align\*\}|\\begin\{alignat\}\{[^}]*\}|\\end\{alignat\}|\\begin\{alignat\*\}\{[^}]*\}|\\end\{alignat\*\}|\\begin\{aligned\}|\\end\{aligned\}|\\begin\{alignedat\}\{[^}]*\}|\\end\{alignedat\}|\\begin\{array\}\{[^}]*\}|\\end\{array\}|\\begin\{eqnarray\}|\\end\{eqnarray\}|\\begin\{eqnarray\*\}|\\end\{eqnarray\*\}|\\begin\{equation\}|\\end\{equation\}|\\begin\{equation\*\}|\\end\{equation\*\}|\\begin\{gather\}|\\end\{gather\}|\\begin\{gather\*\}|\\end\{gather\*\}|\\begin\{gathered\}|\\end\{gathered\}|\\begin\{multline\}|\\end\{multline\}|\\begin\{multline\*\}|\\end\{multline\*\}|\\begin\{split\}|\\end\{split\}|\\begin\{subarray\}\{[^}]*\}|\\end\{subarray\}'

def t__SCRIPT(t):
    r'\\displaystyle|\\textstyle|\\scriptstyle|\\scriptscriptstyle|\\text'

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    return t


# A string containing ignored characters (spaces and tabs)
# cannot be a regex, string is treated as list for performance reasons
t_ignore = '& \t'  # r'\\[a-zA-Z]+|&|\\!|\\:|\\;|\\,| |\t|\\begin\{align\}|\\end\{align\}|\\begin\{align\*\}|\\end\{align\*\}|\\begin\{alignat\}\{[^}]*\}|\\end\{alignat\}|\\begin\{alignat\*\}\{[^}]*\}|\\end\{alignat\*\}|\\begin\{aligned\}|\\end\{aligned\}|\\begin\{alignedat\}\{[^}]*\}|\\end\{alignedat\}|\\begin\{array\}\{[^}]*\}|\\end\{array\}|\\begin\{eqnarray\}|\\end\{eqnarray\}|\\begin\{eqnarray\*\}|\\end\{eqnarray\*\}|\\begin\{equation\}|\\end\{equation\}|\\begin\{equation\*\}|\\end\{equation\*\}|\\begin\{gather\}|\\end\{gather\}|\\begin\{gather\*\}|\\end\{gather\*\}|\\begin\{gathered\}|\\end\{gathered\}|\\begin\{multline\}|\\end\{multline\}|\\begin\{multline\*\}|\\end\{multline\*\}|\\begin\{split\}|\\end\{split\}|\\begin\{subarray\}\{[^}]*\}|\\end\{subarray\}'


# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


# Build the lexer
lexer = lex.lex()
