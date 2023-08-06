"""
    domonic.style
    ====================================

    # TODO - should this be moved to the webapi in a future revision?

"""

from .utils import Utils


class StyleSheet:
    """An object implementing the StyleSheet interface represents a single style sheet.
    CSS style sheets will further implement the more specialized CSSStyleSheet interface.
    """

    def __init__(self):
        self.disabled = True  # a boolean value representing whether the current stylesheet has been applied or not
        self.href = None

    @property
    def href(self):
        """Returns a DOMString representing the location of the stylesheet."""
        return self.href

    @property
    def media(self):
        """Returns a MediaList representing the intended destination medium for style information."""
        raise NotImplementedError

    @property
    def ownerNode(self):
        """Returns a Node associating this style sheet with the current document."""
        raise NotImplementedError

    @property
    def parentStyleSheet(self):
        """Returns a StyleSheet including this one, if any; returns null if there aren't any."""
        raise NotImplementedError

    @property
    def title(self):
        """Returns a DOMString representing the advisory title of the current style sheet."""
        raise NotImplementedError

    @property
    def type(self):
        """Returns a DOMString representing the style sheet language for this style sheet."""
        raise NotImplementedError


class StyleSheetList:
    """An instance of this object can be returned by Document.styleSheets.
    it can be iterated over in a standard for loop over its indices, or converted to an Array.
    """

    def __init__(self):
        self.styleSheets = []
        # self.styleSheets.append(StyleSheet())

    '''
    def _populate_stylesheets_from_document(self):
        """ parse the document to find all the stylesheets and add them to the list.
        """
        # get loaded styles
        # sheets = document.getElementsByTagName("style")
        # for sheet in sheets:
            # get the content of the style sheet
        raise NotImplementedError
    '''

    @property
    def length(self):
        """Returns the number of CSSStyleSheet objects in the collection."""
        return len(self.styleSheets)

    def item(self, index):
        """Returns the CSSStyleSheet object at the index passed in, or null if no item exists for that index."""
        return self.styleSheets[index]


class CSSRule:
    """The CSSRule interface represents a single CSS rule.
    There are several types of rules which inherit properties from CSSRule.

    CSSStyleRule
    CSSImportRule
    CSSMediaRule
    CSSFontFaceRule
    CSSPageRule
    CSSNamespaceRule
    CSSKeyframesRule
    CSSKeyframeRule
    CSSCounterStyleRule
    CSSDocumentRule
    CSSSupportsRule
    CSSFontFeatureValuesRule
    CSSViewportRule
    """

    UNKNOWN_RULE: int = 0
    STYLE_RULE: int = 1
    CHARSET_RULE: int = 2
    IMPORT_RULE: int = 3
    MEDIA_RULE: int = 4
    FONT_FACE_RULE: int = 5
    PAGE_RULE: int = 6
    NAMESPACE_RULE: int = 7
    KEYFRAMES_RULE: int = 8
    KEYFRAME_RULE: int = 9
    COUNTER_STYLE_RULE: int = 10
    SUPPORTS_RULE: int = 11
    FONT_FEATURE_VALUES_RULE: int = 12
    VIEWPORT_RULE: int = 13
    SUPPORTS_CONDITION_RULE: int = 14
    DOCUMENT_RULE: int = 15

    def __init__(self):
        self.parentStyleSheet = None
        self._type = None

    @property
    def cssText(self):
        """Represents the textual representation of the rule, e.g. "h1,h2 { font-size: 16pt }" or "@import 'url'".
        To access or modify parts of the rule (e.g. the value of "font-size" in the example)
        use the properties on the specialized interface for the rule's type.
        """
        pass

    @property
    def parentRule(self):
        """Returns the containing rule, otherwise null. E.g. if this rule is a style rule inside an @media block,
        the parent rule would be that CSSMediaRule."""
        raise NotImplementedError

    def parentStyleSheet(self):
        """Returns the CSSStyleSheet object for the style sheet that contains this rule"""
        raise NotImplementedError

    def type(self):
        """Returns one of the Type constants to determine which type of rule is represented."""
        raise NotImplementedError


class CSSRuleList:
    """A CSSRuleList represents an ordered collection of read-only CSSRule objects.
    While the CSSRuleList object is read-only, and cannot be directly modified,
    it is considered a live object, as the content can change over time.
    """

    def __init__(self) -> None:
        self.rules: list = []
        raise NotImplementedError

    def length(self) -> int:
        """Returns an integer representing the number of CSSRule objects in the collection."""
        raise NotImplementedError

    def item(self, index: int):
        """Gets a single CSSRule."""
        raise NotImplementedError


class CSSStyleSheet(StyleSheet):
    """Creates a new CSSStyleSheet object."""

    def __init__(self):
        super().__init__()
        self.rules: list = []

    @property
    def cssRules():  # -> 'CSSStyleRuleList':
        """Returns a live CSSRuleList which maintains an up-to-date list of the CSSRule objects
        that comprise the stylesheet."""
        # return CSSStyleRuleList()
        raise NotImplementedError

    @property
    def ownerRule(self):
        """If this stylesheet is imported into the document using an @import rule,
        the ownerRule property returns the corresponding CSSImportRule; otherwise, this property's value is null."""
        raise NotImplementedError

    def deleteRule(self, index: int):
        """Deletes the rule at the specified index into the stylesheet's rule list."""
        raise NotImplementedError

    def insertRule(self, rule, index: int):
        """Inserts a new rule at the specified position in the stylesheet,
        given the textual representation of the rule."""
        raise NotImplementedError

    def replace(self):
        """Asynchronously replaces the content of the stylesheet and returns
        a Promise that resolves with the updated CSSStyleSheet."""
        raise NotImplementedError

    def replaceSync(self):
        """Synchronously replaces the content of the stylesheet."""
        raise NotImplementedError

    @property
    def rules(self):
        """The rules property is functionally identical to the standard cssRules property
        it returns a live CSSRuleList which maintains an up-to-date list of all of the rules in the style sheet.
        """
        raise NotImplementedError

    # Legacy methods
    def addRule(self, selectorText, style, index: int):
        """Adds a new rule to the stylesheet given the selector to which the style applies and the style block to apply
        to the matching elements.
        This differs from insertRule(), which takes the textual representation of the entire rule as a single string.
        """
        raise NotImplementedError

    def removeRule(self, index: int):
        """Functionally identical to deleteRule();
        removes the rule at the specified index from the stylesheet's rule list."""
        raise NotImplementedError

    def __str__(self):
        # converts the rules to css code
        return ''.join([str(rule) for rule in self.rules])


class Style(object):
    """[ js syntax styles ]
    # TODO - just add normal float?
    # TODO - consider camel case for hyphen params?
    # TODO - not json serialisable due to the decorators.
    """

    def __init__(self, parent_node=None):
        # print("*** MADE A STYLE11 ***")

        self._members_checked = 0

        self._parent_node = parent_node  # so I can update a tags returned style attributes if a style gets set

        self.alignContent = "normal"
        """Sets or returns the alignment between the lines inside a flexible container
        when the items do not use all available space"""

        self.alignItems = "normal"
        """Sets or returns the alignment for items inside a flexible container"""

        self.alignSelf = "auto"
        """Sets or returns the alignment for selected items inside a flexible container"""

        self.animation = "normal"
        """ shorthand property for all the animation properties below, except the animationPlayState property"""

        self.animationDelay = 0
        """Sets or returns when the animation will start"""

        self.animationDirection = "normal"
        """Sets or returns whether or not the animation should play in reverse on alternate cycles"""

        self.animationDuration = 0
        """Sets or returns how many seconds or milliseconds an animation takes to complete one cycle"""

        self.animationFillMode = None
        """Sets or returns what values are applied by the animation outside the time it is executing"""

        self.animationIterationCount = 1
        """Sets or returns the number of times an animation should be played"""

        self.animationName = None
        """Sets or returns a name for the @keyframes animation"""

        self.animationTimingFunction = "ease"
        """Sets or returns the speed curve of the animation"""

        self.animationPlayState = "running"
        """Sets or returns whether the animation is running or paused """

        self.background = None
        """Sets or returns all the background properties in one declaration"""

        self.backgroundAttachment = "scroll"
        """Sets or returns whether a background-image is fixed or scrolls with the page"""

        self.backgroundColor = None
        """Sets or returns the background-color of an element """

        self.backgroundImage = None
        """Sets or returns the background-image for an element"""

        self.backgroundPosition = None
        """Sets or returns the starting position of a background-image"""

        self.backgroundRepeat = None
        """Sets or returns how to repeat (tile) a background-image"""

        self.backgroundClip = None
        """Sets or returns the painting area of the background"""

        self.backgroundOrigin = None
        """Sets or returns the positioning area of the background images"""

        self.backgroundSize = None
        """Sets or returns the size of the background image"""

        self.backfaceVisibility = None
        """Sets or returns whether or not an element should be visible when not facing the screen """

        self.border = "medium none black"
        """Sets or returns borderWidth, borderStyle, and borderColor in one declaration"""

        self.borderBottom = "medium none black"
        """Sets or returns all the borderBottom properties in one declaration """

        self.borderBottomColor = None
        """Sets or returns the color of the bottom border  1 """

        self.borderBottomLeftRadius = 0
        """Sets or returns the shape of the border of the bottom-left corner"""

        self.borderBottomRightRadius = 0
        """Sets or returns the shape of the border of the bottom-right corner """

        self.borderBottomStyle = None
        """Sets or returns the style of the bottom border """

        self.borderBottomWidth = None
        """Sets or returns the width of the bottom border """

        self.borderCollapse = None
        """Sets or returns whether the table border should be collapsed into a single border, or not"""

        self.borderColor = None
        """Sets or returns the color of an element's border (can have up to four values)"""

        self.borderImage = None
        """horthand property for setting or returning all the borderImage properties"""

        self.borderImageOutset = None
        """Sets or returns the amount by which the border image area extends beyond the border box"""

        self.borderImageRepeat = None
        """Sets or returns whether the image-border should be repeated, rounded or stretched"""

        self.borderImageSlice = None
        """Sets or returns the inward offsets of the image-border """

        self.borderImageSource = None
        """Sets or returns the image to be used as a border"""

        self.borderImageWidth = None
        """Sets or returns the widths of the image-border """

        self.borderLeft = None
        """Sets or returns all the borderLeft properties in one declaration"""

        self.borderLeftColor = None
        """Sets or returns the color of the left border"""

        self.borderLeftStyle = None
        """Sets or returns the style of the left border"""

        self.borderLeftWidth = None
        """Sets or returns the width of the left border"""

        self.borderRadius = 0
        """A shorthand property for setting or returning all the four borderRadius properties """

        self.borderRight = None
        """Sets or returns all the borderRight properties in one declaration"""

        self.borderRightColor = None
        """Sets or returns the color of the right border"""

        self.borderRightStyle = None
        """Sets or returns the style of the right border"""

        self.borderRightWidth = None
        """Sets or returns the width of the right border"""

        self.borderSpacing = None
        """Sets or returns the space between cells in a table """

        self.borderStyle = None
        """Sets or returns the style of an element's border (can have up to four values)"""

        self.borderTop = None
        """Sets or returns all the borderTop properties in one declaration"""

        self.borderTopColor = None
        """Sets or returns the color of the top border"""

        self.borderTopLeftRadius = 0
        """Sets or returns the shape of the border of the top-left corner """

        self.borderTopRightRadius = 0
        """Sets or returns the shape of the border of the top-right corner"""

        self.borderTopStyle = None
        """Sets or returns the style of the top border"""

        self.borderTopWidth = None
        """Sets or returns the width of the top border"""

        self.borderWidth = None
        """Sets or returns the width of an element's border (can have up to four values)"""

        self.bottom = None
        """Sets or returns the bottom position of a positioned element"""

        self.boxDecorationBreak = None
        """Sets or returns the behaviour of the background and border of an element at page-break, or,
        for in-line elements, at line-break."""

        self.boxShadow = None
        """ttaches one or more drop-shadows to the box"""

        self.boxSizing = None
        """llows you to define certain elements to fit an area in a certain way"""

        self.captionSide = None
        """Sets or returns the position of the table caption"""

        self.clear = None
        """Sets or returns the position of the element relative to floating objects"""

        self.clip = None
        """Sets or returns which part of a positioned element is visible"""

        self.color = None
        """Sets or returns the color of the text"""

        self.columnCount = None
        """Sets or returns the number of columns an element should be divided into"""

        self.columnFill = None
        """Sets or returns how to fill columns"""

        self.columnGap = "normal"
        """Sets or returns the gap between the columns"""

        self.columnRule = None
        """shorthand property for setting or returning all the columnRule properties"""

        self.columnRuleColor = None
        """Sets or returns the color of the rule between columns"""

        self.columnRuleStyle = None
        """Sets or returns the style of the rule between columns"""

        self.columnRuleWidth = None
        """Sets or returns the width of the rule between columns"""

        self.columns = None
        """horthand property for setting or returning columnWidth and columnCount"""

        self.columnSpan = None
        """Sets or returns how many columns an element should span across """

        self.columnWidth = None
        """Sets or returns the width of the columns"""

        self.content = None
        """d with the :before and :after pseudo-elements, to insert generated content"""

        self.counterIncrement = None
        """Increments one or more counters"""

        self.counterReset = None
        """Creates or resets one or more counters """

        self.cursor = None
        """Sets or returns the type of cursor to display for the mouse pointer"""

        self.direction = None
        """Sets or returns the text direction """

        self.display = None
        """Sets or returns an element's display type"""

        self.emptyCells = None
        """Sets or returns whether to show the border and background of empty cells, or not """

        self.filter = None
        """Sets or returns image filters (visual effects, like blur and saturation)"""

        self.flex = None
        """Sets or returns the length of the item, relative to the rest"""

        self.flexBasis = None
        """Sets or returns the initial length of a flexible item"""

        self.flexDirection = None
        """Sets or returns the direction of the flexible items"""

        self.flexFlow = None
        """A shorthand property for the flexDirection and the flexWrap properties """

        self.flexGrow = None
        """Sets or returns how much the item will grow relative to the rest"""

        self.flexShrink = None
        """Sets or returns how the item will shrink relative to the rest"""

        self.flexWrap = None
        """Sets or returns whether the flexible items should wrap or not"""

        self.float = None  # ADDED BY ME

        self.cssFloat = None
        """Sets or returns the horizontal alignment of an element """

        self.font = None
        """Sets or returns fontStyle, fontVariant, fontWeight, fontSize, lineHeight, and fontFamily
        in one declaration"""

        self.fontFamily = None
        """Sets or returns the font family for text"""

        self.fontSize = "medium"
        """Sets or returns the font size of the text"""

        self.fontStyle = "normal"
        """Sets or returns whether the style of the font is normal, italic or oblique """

        self.fontVariant = None
        """Sets or returns whether the font should be displayed in small capital letters"""

        self.fontWeight = "normal"
        """Sets or returns the boldness of the font"""

        self.fontSizeAdjust = None
        """eserves the readability of text when font fallback occurs"""

        self.fontStretch = None
        """ects a normal, condensed, or expanded face from a font family"""

        self.hangingPunctuation = None
        """ecifies whether a punctuation character may be placed outside the line box"""

        self.height = "auto"
        """Sets or returns the height of an element"""

        self.hyphens = None
        """Sets how to split words to improve the layout of paragraphs"""

        self.icon = None
        """Provides the author the ability to style an element with an iconic equivalent"""

        self.imageOrientation = None
        """Specifies a rotation in the right or clockwise direction that a user agent applies to an image """

        self.isolation = None
        """efines whether an element must create a new stacking content"""

        self.justifyContent = "normal"
        """Sets or returns the alignment between the items inside a flexible container when the items
        do not use all available space. """

        self.left = "auto"
        """Sets or returns the left position of a positioned element"""

        self.letterSpacing = None
        """Sets or returns the space between characters in a text """

        self.lineHeight = None
        """Sets or returns the distance between lines in a text"""

        self.listStyle = None
        """Sets or returns listStyleImage, listStylePosition, and listStyleType in one declaration"""

        self.listStyleImage = None
        """Sets or returns an image as the list-item marker"""

        self.listStylePosition = None
        """Sets or returns the position of the list-item marker"""

        self.listStyleType = None
        """Sets or returns the list-item marker type"""

        self.margin = 0
        """Sets or returns the margins of an element (can have up to four values) """

        self.marginBottom = 0
        """Sets or returns the bottom margin of an element"""

        self.marginLeft = 0
        """Sets or returns the left margin of an element"""

        self.marginRight = 0
        """Sets or returns the right margin of an element """

        self.marginTop = 0
        """Sets or returns the top margin of an element"""

        self.maxHeight = None
        """Sets or returns the maximum height of an element """

        self.maxWidth = None
        """Sets or returns the maximum width of an element"""

        self.minHeight = None
        """Sets or returns the minimum height of an element """

        self.minWidth = None
        """Sets or returns the minimum width of an element"""

        self.navDown = None
        """Sets or returns where to navigate when using the arrow-down navigation key """

        self.navIndex = None
        """Sets or returns the tabbing order for an element"""

        self.navLeft = None
        """Sets or returns where to navigate when using the arrow-left navigation key """

        self.navRight = None
        """Sets or returns where to navigate when using the arrow-right navigation key"""

        self.navUp = None
        """Sets or returns where to navigate when using the arrow-up navigation key"""

        self.objectFit = None
        """pecifies how the contents of a replaced element should be fitted to the box
        established by its used height and width"""

        self.objectPosition = None
        """ecifies the alignment of the replaced element inside its box """

        self.opacity = None
        """Sets or returns the opacity level for an element"""

        self.order = None
        """Sets or returns the order of the flexible item, relative to the rest"""

        self.orphans = None
        """Sets or returns the minimum number of lines for an element that must be left at the bottom
        of a page when a page break occurs inside an element"""

        self.outline = None
        """Sets or returns all the outline properties in one declaration"""

        self.outlineColor = None
        """Sets or returns the color of the outline around a element"""

        self.outlineOffset = None
        """ffsets an outline, and draws it beyond the border edge"""

        self.outlineStyle = None
        """Sets or returns the style of the outline around an element """

        self.outlineWidth = None
        """Sets or returns the width of the outline around an element """

        self.overflow = "visible"
        """Sets or returns what to do with content that renders outside the element box """

        self.overflowX = None
        """pecifies what to do with the left/right edges of the content, if it overflows the element's content area"""

        self.overflowY = None
        """pecifies what to do with the top/bottom edges of the content, if it overflows the element's content area"""

        self.padding = 0
        """Sets or returns the padding of an element (can have up to four values) """

        self.paddingBottom = 0
        """Sets or returns the bottom padding of an element"""

        self.paddingLeft = 0
        """Sets or returns the left padding of an element """

        self.paddingRight = 0
        """Sets or returns the right padding of an element"""

        self.paddingTop = 0
        """Sets or returns the top padding of an element"""

        self.pageBreakAfter = "auto"
        """Sets or returns the page-break behavior after an element """

        self.pageBreakBefore = "auto"
        """Sets or returns the page-break behavior before an element"""

        self.pageBreakInside = "auto"
        """Sets or returns the page-break behavior inside an element"""

        self.perspective = None
        """Sets or returns the perspective on how 3D elements are viewed"""

        self.perspectiveOrigin = None
        """Sets or returns the bottom position of 3D elements """

        self.position = None
        """Sets or returns the type of positioning method used for an element (static, relative, absolute or fixed) """

        self.quotes = None
        """Sets or returns the type of quotation marks for embedded quotations"""

        self.resize = None
        """Sets or returns whether or not an element is resizable by the user """

        self.right = "auto"
        """Sets or returns the right position of a positioned element """

        self.tableLayout = "auto"
        """Sets or returns the way to lay out table cells, rows, and columns"""

        self.tabSize = None
        """Sets or returns the length of the tab-character"""

        self.textAlign = "left"
        """Sets or returns the horizontal alignment of text"""

        self.textAlignLast = "auto"
        """Sets or returns how the last line of a block or a line right before a forced line break
        is aligned when text-align is justify"""

        self.textDecoration = None
        """Sets or returns the decoration of a text"""

        self.textDecorationColor = None
        """Sets or returns the color of the text-decoration"""

        self.textDecorationLine = None
        """Sets or returns the type of line in a text-decoration"""

        self.textDecorationStyle = None
        """Sets or returns the style of the line in a text decoration """

        self.textIndent = None
        """Sets or returns the indentation of the first line of text"""

        self.textJustify = None
        """Sets or returns the justification method used when text-align is justify"""

        self.textOverflow = "clip"
        """Sets or returns what should happen when text overflows the containing element"""

        self.textShadow = None
        """Sets or returns the shadow effect of a text"""

        self.textTransform = None
        """Sets or returns the capitalization of a text"""

        self.top = None
        """Sets or returns the top position of a positioned element """

        self.transform = None
        """pplies a 2D or 3D transformation to an element"""

        self.transformOrigin = None
        """Sets or returns the position of transformed elements"""

        self.transformStyle = None
        """Sets or returns how nested elements are rendered in 3D space"""

        self.transition = None
        """shorthand property for setting or returning the four transition properties"""

        self.transitionProperty = None
        """Sets or returns the CSS property that the transition effect is for """

        self.transitionDuration = 0
        """Sets or returns how many seconds or milliseconds a transition effect takes to complete """

        self.transitionTimingFunction = None
        """Sets or returns the speed curve of the transition effect"""

        self.transitionDelay = 0
        """Sets or returns when the transition effect will start"""

        self.unicodeBidi = None
        """Sets or returns whether the text should be overridden to support multiple languages in the same document """

        self.userSelect = None
        """Sets or returns whether the text of an element can be selected or not"""

        self.verticalAlign = None
        """Sets or returns the vertical alignment of the content in an element"""

        self.visibility = "visible"
        """Sets or returns whether an element should be visible"""

        self.whiteSpace = "normal"
        """ Sets or returns how to handle tabs, line breaks and whitespace in a text 1 """

        self.width = "auto"
        """Sets or returns the width of an element"""

        self.wordBreak = "normal"
        """Sets or returns line breaking rules for non-CJK scripts"""

        self.wordSpacing = None
        """Sets or returns the spacing between words in a text"""

        self.wordWrap = "normal"
        """Allows long, unbreakable words to be broken and wrap to the next line"""

        self.widows = None
        """Sets or returns the minimum number of lines for an element that must be visible at the top of a page """

        self.zIndex = "auto"
        """Sets or returns the stack order of a positioned element"""

    def style_set_decorator(func):
        from functools import wraps

        @wraps(func)
        def style_wrapper(self, *args, **kwargs):
            value = args[0]
            if value is None:
                value = "none"
            func(self, value, *args, **kwargs)

            self._members_checked += 1
            if self._members_checked < len(vars(self)) - 1:
                return

            if self._parent_node is not None:
                s = f"{Utils.case_kebab(func.__name__)}:{value};"
                styles = self._parent_node.getAttribute("style")
                # print('sup:', styles)

                if styles is not None:
                    # TODO - replace if exists
                    styles = styles + s
                else:
                    styles = s

                # print(styles)
                self._parent_node.setAttribute("style", styles)

        return style_wrapper

    def style_get_decorator(func):
        from functools import wraps

        @wraps(func)
        def style_wrapper(value=None, *args, **kwargs):
            value = func(value, *args, **kwargs)
            if value is None:
                value = "none"
            return value

        return style_wrapper

    @property
    @style_get_decorator  # TODO - pass array of valid words as params. so can raise value errors
    def alignContent(self):
        return self.__alignContent

    @alignContent.setter
    @style_set_decorator
    def alignContent(self, value="stretch", *args, **kwargs):
        self.__alignContent = value

    @property
    @style_get_decorator
    def alignItems(self):
        return self.__alignItems

    @alignItems.setter
    @style_set_decorator
    def alignItems(self, value=None, *args, **kwargs):
        self.__alignItems = value

    @property
    @style_get_decorator
    def alignSelf(self):
        return self.__alignSelf

    @alignSelf.setter
    @style_set_decorator
    def alignSelf(self, value=None, *args, **kwargs):
        self.__alignSelf = value

    @property
    @style_get_decorator
    def animation(self):
        return self.__animation

    @animation.setter
    @style_set_decorator
    def animation(self, value=None, *args, **kwargs):
        self.__animation = value

    @property
    @style_get_decorator
    def animationDelay(self):
        return self.__animationDelay

    @animationDelay.setter
    @style_set_decorator
    def animationDelay(self, value=None, *args, **kwargs):
        self.__animationDelay = value

    @property
    @style_get_decorator
    def animationDirection(self):
        return self.__animationDirection

    @animationDirection.setter
    @style_set_decorator
    def animationDirection(self, value=None, *args, **kwargs):
        self.__animationDirection = value

    @property
    @style_get_decorator
    def animationDuration(self):
        return self.__animationDuration

    @animationDuration.setter
    @style_set_decorator
    def animationDuration(self, value=None, *args, **kwargs):
        self.__animationDuration = value

    @property
    @style_get_decorator
    def animationFillMode(self):
        return self.__animationFillMode

    @animationFillMode.setter
    @style_set_decorator
    def animationFillMode(self, value=None, *args, **kwargs):
        self.__animationFillMode = value

    @property
    @style_get_decorator
    def animationIterationCount(self):
        return self.__animationIterationCount

    @animationIterationCount.setter
    @style_set_decorator
    def animationIterationCount(self, value=None, *args, **kwargs):
        self.__animationIterationCount = value

    @property
    @style_get_decorator
    def animationName(self):
        return self.__animationName

    @animationName.setter
    @style_set_decorator
    def animationName(self, value=None, *args, **kwargs):
        self.__animationName = value

    @property
    @style_get_decorator
    def animationTimingFunction(self):
        return self.__animationTimingFunction

    @animationTimingFunction.setter
    @style_set_decorator
    def animationTimingFunction(self, value=None, *args, **kwargs):
        self.__animationTimingFunction = value

    @property
    @style_get_decorator
    def animationPlayState(self):
        return self.__animationPlayState

    @animationPlayState.setter
    @style_set_decorator
    def animationPlayState(self, value=None, *args, **kwargs):
        self.__animationPlayState = value

    @property
    @style_get_decorator
    def background(self):
        return self.__background

    @background.setter
    @style_set_decorator
    def background(self, value=None, *args, **kwargs):
        self.__background = value

    @property
    @style_get_decorator
    def backgroundAttachment(self):
        return self.__backgroundAttachment

    @backgroundAttachment.setter
    @style_set_decorator
    def backgroundAttachment(self, value=None, *args, **kwargs):
        self.__backgroundAttachment = value

    @property
    @style_get_decorator
    def backgroundColor(self):
        return self.__backgroundColor

    @backgroundColor.setter
    @style_set_decorator
    def backgroundColor(self, value=None, *args, **kwargs):
        self.__backgroundColor = value

    @property
    @style_get_decorator
    def backgroundImage(self):
        return self.__backgroundImage

    @backgroundImage.setter
    @style_set_decorator
    def backgroundImage(self, value=None, *args, **kwargs):
        self.__backgroundImage = value

    @property
    @style_get_decorator
    def backgroundPosition(self):
        return self.__backgroundPosition

    @backgroundPosition.setter
    @style_set_decorator
    def backgroundPosition(self, value=None, *args, **kwargs):
        self.__backgroundPosition = value

    @property
    @style_get_decorator
    def backgroundRepeat(self):
        return self.__backgroundRepeat

    @backgroundRepeat.setter
    @style_set_decorator
    def backgroundRepeat(self, value=None, *args, **kwargs):
        self.__backgroundRepeat = value

    @property
    @style_get_decorator
    def backgroundClip(self):
        return self.__backgroundClip

    @backgroundClip.setter
    @style_set_decorator
    def backgroundClip(self, value=None, *args, **kwargs):
        self.__backgroundClip = value

    @property
    @style_get_decorator
    def backgroundOrigin(self):
        return self.__backgroundOrigin

    @backgroundOrigin.setter
    @style_set_decorator
    def backgroundOrigin(self, value=None, *args, **kwargs):
        self.__backgroundOrigin = value

    @property
    @style_get_decorator
    def backgroundSize(self):
        return self.__backgroundSize

    @backgroundSize.setter
    @style_set_decorator
    def backgroundSize(self, value=None, *args, **kwargs):
        self.__backgroundSize = value

    @property
    @style_get_decorator
    def backfaceVisibility(self):
        return self.__backfaceVisibility

    @backfaceVisibility.setter
    @style_set_decorator
    def backfaceVisibility(self, value=None, *args, **kwargs):
        self.__backfaceVisibility = value

    @property
    @style_get_decorator
    def border(self):
        return self.__border

    @border.setter
    @style_set_decorator
    def border(self, value=None, *args, **kwargs):
        self.__border = value

    @property
    @style_get_decorator
    def borderBottom(self):
        return self.__borderBottom

    @borderBottom.setter
    @style_set_decorator
    def borderBottom(self, value=None, *args, **kwargs):
        self.__borderBottom = value

    @property
    @style_get_decorator
    def borderBottomColor(self):
        return self.__borderBottomColor

    @borderBottomColor.setter
    @style_set_decorator
    def borderBottomColor(self, value=None, *args, **kwargs):
        self.__borderBottomColor = value

    @property
    @style_get_decorator
    def borderBottomLeftRadius(self):
        return self.__borderBottomLeftRadius

    @borderBottomLeftRadius.setter
    @style_set_decorator
    def borderBottomLeftRadius(self, value=None, *args, **kwargs):
        self.__borderBottomLeftRadius = value

    @property
    @style_get_decorator
    def borderBottomRightRadius(self):
        return self.__borderBottomRightRadius

    @borderBottomRightRadius.setter
    @style_set_decorator
    def borderBottomRightRadius(self, value=None, *args, **kwargs):
        self.__borderBottomRightRadius = value

    @property
    @style_get_decorator
    def borderBottomStyle(self):
        return self.__borderBottomStyle

    @borderBottomStyle.setter
    @style_set_decorator
    def borderBottomStyle(self, value=None, *args, **kwargs):
        self.__borderBottomStyle = value

    @property
    @style_get_decorator
    def borderBottomWidth(self):
        return self.__borderBottomWidth

    @borderBottomWidth.setter
    @style_set_decorator
    def borderBottomWidth(self, value=None, *args, **kwargs):
        self.__borderBottomWidth = value

    @property
    @style_get_decorator
    def borderCollapse(self):
        return self.__borderCollapse

    @borderCollapse.setter
    @style_set_decorator
    def borderCollapse(self, value=None, *args, **kwargs):
        self.__borderCollapse = value

    @property
    @style_get_decorator
    def borderColor(self):
        return self.__borderColor

    @borderColor.setter
    @style_set_decorator
    def borderColor(self, value=None, *args, **kwargs):
        self.__borderColor = value

    @property
    @style_get_decorator
    def borderImage(self):
        return self.__borderImage

    @borderImage.setter
    @style_set_decorator
    def borderImage(self, value=None, *args, **kwargs):
        self.__borderImage = value

    @property
    @style_get_decorator
    def borderImageOutset(self):
        return self.__borderImageOutset

    @borderImageOutset.setter
    @style_set_decorator
    def borderImageOutset(self, value=None, *args, **kwargs):
        self.__borderImageOutset = value

    @property
    @style_get_decorator
    def borderImageRepeat(self):
        return self.__borderImageRepeat

    @borderImageRepeat.setter
    @style_set_decorator
    def borderImageRepeat(self, value=None, *args, **kwargs):
        self.__borderImageRepeat = value

    @property
    @style_get_decorator
    def borderImageSlice(self):
        return self.__borderImageSlice

    @borderImageSlice.setter
    @style_set_decorator
    def borderImageSlice(self, value=None, *args, **kwargs):
        self.__borderImageSlice = value

    @property
    @style_get_decorator
    def borderImageSource(self):
        return self.__borderImageSource

    @borderImageSource.setter
    @style_set_decorator
    def borderImageSource(self, value=None, *args, **kwargs):
        self.__borderImageSource = value

    @property
    @style_get_decorator
    def borderImageWidth(self):
        return self.__borderImageWidth

    @borderImageWidth.setter
    @style_set_decorator
    def borderImageWidth(self, value=None, *args, **kwargs):
        self.__borderImageWidth = value

    @property
    @style_get_decorator
    def borderLeft(self):
        return self.__borderLeft

    @borderLeft.setter
    @style_set_decorator
    def borderLeft(self, value=None, *args, **kwargs):
        self.__borderLeft = value

    @property
    @style_get_decorator
    def borderLeftColor(self):
        return self.__borderLeftColor

    @borderLeftColor.setter
    @style_set_decorator
    def borderLeftColor(self, value=None, *args, **kwargs):
        self.__borderLeftColor = value

    @property
    @style_get_decorator
    def borderLeftStyle(self):
        return self.__borderLeftStyle

    @borderLeftStyle.setter
    @style_set_decorator
    def borderLeftStyle(self, value=None, *args, **kwargs):
        self.__borderLeftStyle = value

    @property
    @style_get_decorator
    def borderLeftWidth(self):
        return self.__borderLeftWidth

    @borderLeftWidth.setter
    @style_set_decorator
    def borderLeftWidth(self, value=None, *args, **kwargs):
        self.__borderLeftWidth = value

    @property
    @style_get_decorator
    def borderRadius(self):
        return self.__borderRadius

    @borderRadius.setter
    @style_set_decorator
    def borderRadius(self, value=None, *args, **kwargs):
        self.__borderRadius = value

    @property
    @style_get_decorator
    def borderRight(self):
        return self.__borderRight

    @borderRight.setter
    @style_set_decorator
    def borderRight(self, value=None, *args, **kwargs):
        self.__borderRight = value

    @property
    @style_get_decorator
    def borderRightColor(self):
        return self.__borderRightColor

    @borderRightColor.setter
    @style_set_decorator
    def borderRightColor(self, value=None, *args, **kwargs):
        self.__borderRightColor = value

    @property
    @style_get_decorator
    def borderRightStyle(self):
        return self.__borderRightStyle

    @borderRightStyle.setter
    @style_set_decorator
    def borderRightStyle(self, value=None, *args, **kwargs):
        self.__borderRightStyle = value

    @property
    @style_get_decorator
    def borderRightWidth(self):
        return self.__borderRightWidth

    @borderRightWidth.setter
    @style_set_decorator
    def borderRightWidth(self, value=None, *args, **kwargs):
        self.__borderRightWidth = value

    @property
    @style_get_decorator
    def borderSpacing(self):
        return self.__borderSpacing

    @borderSpacing.setter
    @style_set_decorator
    def borderSpacing(self, value=None, *args, **kwargs):
        self.__borderSpacing = value

    @property
    @style_get_decorator
    def borderStyle(self):
        return self.__borderStyle

    @borderStyle.setter
    @style_set_decorator
    def borderStyle(self, value=None, *args, **kwargs):
        self.__borderStyle = value

    @property
    @style_get_decorator
    def borderTop(self):
        return self.__borderTop

    @borderTop.setter
    @style_set_decorator
    def borderTop(self, value=None, *args, **kwargs):
        self.__borderTop = value

    @property
    @style_get_decorator
    def borderTopColor(self):
        return self.__borderTopColor

    @borderTopColor.setter
    @style_set_decorator
    def borderTopColor(self, value=None, *args, **kwargs):
        self.__borderTopColor = value

    @property
    @style_get_decorator
    def borderTopLeftRadius(self):
        return self.__borderTopLeftRadius

    @borderTopLeftRadius.setter
    @style_set_decorator
    def borderTopLeftRadius(self, value=None, *args, **kwargs):
        self.__borderTopLeftRadius = value

    @property
    @style_get_decorator
    def borderTopRightRadius(self):
        return self.__borderTopRightRadius

    @borderTopRightRadius.setter
    @style_set_decorator
    def borderTopRightRadius(self, value=None, *args, **kwargs):
        self.__borderTopRightRadius = value

    @property
    @style_get_decorator
    def borderTopStyle(self):
        return self.__borderTopStyle

    @borderTopStyle.setter
    @style_set_decorator
    def borderTopStyle(self, value=None, *args, **kwargs):
        self.__borderTopStyle = value

    @property
    @style_get_decorator
    def borderTopWidth(self):
        return self.__borderTopWidth

    @borderTopWidth.setter
    @style_set_decorator
    def borderTopWidth(self, value=None, *args, **kwargs):
        self.__borderTopWidth = value

    @property
    @style_get_decorator
    def borderWidth(self):
        return self.__borderWidth

    @borderWidth.setter
    @style_set_decorator
    def borderWidth(self, value=None, *args, **kwargs):
        self.__borderWidth = value

    @property
    @style_get_decorator
    def bottom(self):
        return self.__bottom

    @bottom.setter
    @style_set_decorator
    def bottom(self, value=None, *args, **kwargs):
        self.__bottom = value

    @property
    @style_get_decorator
    def boxDecorationBreak(self):
        return self.__boxDecorationBreak

    @boxDecorationBreak.setter
    @style_set_decorator
    def boxDecorationBreak(self, value=None, *args, **kwargs):
        self.__boxDecorationBreak = value

    @property
    @style_get_decorator
    def boxShadow(self):
        return self.__boxShadow

    @boxShadow.setter
    @style_set_decorator
    def boxShadow(self, value=None, *args, **kwargs):
        self.__boxShadow = value

    @property
    @style_get_decorator
    def boxSizing(self):
        return self.__boxSizing

    @boxSizing.setter
    @style_set_decorator
    def boxSizing(self, value=None, *args, **kwargs):
        self.__boxSizing = value

    @property
    @style_get_decorator
    def captionSide(self):
        return self.__captionSide

    @captionSide.setter
    @style_set_decorator
    def captionSide(self, value=None, *args, **kwargs):
        self.__captionSide = value

    @property
    @style_get_decorator
    def clear(self):
        return self.__clear

    @clear.setter
    @style_set_decorator
    def clear(self, value=None, *args, **kwargs):
        self.__clear = value

    @property
    @style_get_decorator
    def clip(self):
        return self.__clip

    @clip.setter
    @style_set_decorator
    def clip(self, value=None, *args, **kwargs):
        self.__clip = value

    @property
    @style_get_decorator
    def color(self):
        return self.__color

    @color.setter
    @style_set_decorator
    def color(self, value=None, *args, **kwargs):
        self.__color = value

    @property
    @style_get_decorator
    def columnCount(self):
        return self.__columnCount

    @columnCount.setter
    @style_set_decorator
    def columnCount(self, value=None, *args, **kwargs):
        self.__columnCount = value

    @property
    @style_get_decorator
    def columnFill(self):
        return self.__columnFill

    @columnFill.setter
    @style_set_decorator
    def columnFill(self, value=None, *args, **kwargs):
        self.__columnFill = value

    @property
    @style_get_decorator
    def columnGap(self):
        return self.__columnGap

    @columnGap.setter
    @style_set_decorator
    def columnGap(self, value=None, *args, **kwargs):
        self.__columnGap = value

    @property
    @style_get_decorator
    def columnRule(self):
        return self.__columnRule

    @columnRule.setter
    @style_set_decorator
    def columnRule(self, value=None, *args, **kwargs):
        self.__columnRule = value

    @property
    @style_get_decorator
    def columnRuleColor(self):
        return self.__columnRuleColor

    @columnRuleColor.setter
    @style_set_decorator
    def columnRuleColor(self, value=None, *args, **kwargs):
        self.__columnRuleColor = value

    @property
    @style_get_decorator
    def columnRuleStyle(self):
        return self.__columnRuleStyle

    @columnRuleStyle.setter
    @style_set_decorator
    def columnRuleStyle(self, value=None, *args, **kwargs):
        self.__columnRuleStyle = value

    @property
    @style_get_decorator
    def columnRuleWidth(self):
        return self.__columnRuleWidth

    @columnRuleWidth.setter
    @style_set_decorator
    def columnRuleWidth(self, value=None, *args, **kwargs):
        self.__columnRuleWidth = value

    @property
    @style_get_decorator
    def columns(self):
        return self.__columns

    @columns.setter
    @style_set_decorator
    def columns(self, value=None, *args, **kwargs):
        self.__columns = value

    @property
    @style_get_decorator
    def columnSpan(self):
        return self.__columnSpan

    @columnSpan.setter
    @style_set_decorator
    def columnSpan(self, value=None, *args, **kwargs):
        self.__columnSpan = value

    @property
    @style_get_decorator
    def columnWidth(self):
        return self.__columnWidth

    @columnWidth.setter
    @style_set_decorator
    def columnWidth(self, value=None, *args, **kwargs):
        self.__columnWidth = value

    @property
    @style_get_decorator
    def content(self):
        return self.__content

    @content.setter
    @style_set_decorator
    def content(self, value=None, *args, **kwargs):
        self.__content = value

    @property
    @style_get_decorator
    def counterIncrement(self):
        return self.__counterIncrement

    @counterIncrement.setter
    @style_set_decorator
    def counterIncrement(self, value=None, *args, **kwargs):
        self.__counterIncrement = value

    @property
    @style_get_decorator
    def counterReset(self):
        return self.__counterReset

    @counterReset.setter
    @style_set_decorator
    def counterReset(self, value=None, *args, **kwargs):
        self.__counterReset = value

    @property
    @style_get_decorator
    def cursor(self):
        return self.__cursor

    @cursor.setter
    @style_set_decorator
    def cursor(self, value=None, *args, **kwargs):
        self.__cursor = value

    @property
    @style_get_decorator
    def direction(self):
        return self.__direction

    @direction.setter
    @style_set_decorator
    def direction(self, value=None, *args, **kwargs):
        self.__direction = value

    @property
    @style_get_decorator
    def display(self):
        return self.__display

    @display.setter
    @style_set_decorator
    def display(self, value=None, *args, **kwargs):
        self.__display = value

    @property
    @style_get_decorator
    def emptyCells(self):
        return self.__emptyCells

    @emptyCells.setter
    @style_set_decorator
    def emptyCells(self, value=None, *args, **kwargs):
        self.__emptyCells = value

    @property
    @style_get_decorator
    def filter(self):
        return self.__filter

    @filter.setter
    @style_set_decorator
    def filter(self, value=None, *args, **kwargs):
        self.__filter = value

    @property
    @style_get_decorator
    def flex(self):
        return self.__flex

    @flex.setter
    @style_set_decorator
    def flex(self, value=None, *args, **kwargs):
        self.__flex = value

    @property
    @style_get_decorator
    def flexBasis(self):
        return self.__flexBasis

    @flexBasis.setter
    @style_set_decorator
    def flexBasis(self, value=None, *args, **kwargs):
        self.__flexBasis = value

    @property
    @style_get_decorator
    def flexDirection(self):
        return self.__flexDirection

    @flexDirection.setter
    @style_set_decorator
    def flexDirection(self, value=None, *args, **kwargs):
        self.__flexDirection = value

    @property
    @style_get_decorator
    def flexFlow(self):
        return self.__flexFlow

    @flexFlow.setter
    @style_set_decorator
    def flexFlow(self, value=None, *args, **kwargs):
        self.__flexFlow = value

    @property
    @style_get_decorator
    def flexGrow(self):
        return self.__flexGrow

    @flexGrow.setter
    @style_set_decorator
    def flexGrow(self, value=None, *args, **kwargs):
        self.__flexGrow = value

    @property
    @style_get_decorator
    def flexShrink(self):
        return self.__flexShrink

    @flexShrink.setter
    @style_set_decorator
    def flexShrink(self, value=None, *args, **kwargs):
        self.__flexShrink = value

    @property
    @style_get_decorator
    def flexWrap(self):
        return self.__flexWrap

    @flexWrap.setter
    @style_set_decorator
    def flexWrap(self, value=None, *args, **kwargs):
        self.__flexWrap = value

    @property
    @style_get_decorator
    def float(self):
        return self.__float

    @float.setter
    @style_set_decorator
    def float(self, value=None, *args, **kwargs):
        self.__float = value

    @property
    @style_get_decorator
    def cssFloat(self):
        return self.__cssFloat

    @cssFloat.setter
    @style_set_decorator
    def cssFloat(self, value=None, *args, **kwargs):
        self.__cssFloat = value

    @property
    @style_get_decorator
    def font(self):
        return self.__font

    @font.setter
    @style_set_decorator
    def font(self, value=None, *args, **kwargs):
        self.__font = value

    @property
    @style_get_decorator
    def fontFamily(self):
        return self.__fontFamily

    @fontFamily.setter
    @style_set_decorator
    def fontFamily(self, value=None, *args, **kwargs):
        self.__fontFamily = value

    @property
    @style_get_decorator
    def fontSize(self):
        return self.__fontSize

    @fontSize.setter
    @style_set_decorator
    def fontSize(self, value=None, *args, **kwargs):
        self.__fontSize = value

    @property
    @style_get_decorator
    def fontStyle(self):
        return self.__fontStyle

    @fontStyle.setter
    @style_set_decorator
    def fontStyle(self, value=None, *args, **kwargs):
        self.__fontStyle = value

    @property
    @style_get_decorator
    def fontVariant(self):
        return self.__fontVariant

    @fontVariant.setter
    @style_set_decorator
    def fontVariant(self, value=None, *args, **kwargs):
        self.__fontVariant = value

    @property
    @style_get_decorator
    def fontWeight(self):
        return self.__fontWeight

    @fontWeight.setter
    @style_set_decorator
    def fontWeight(self, value=None, *args, **kwargs):
        self.__fontWeight = value

    @property
    @style_get_decorator
    def fontSizeAdjust(self):
        return self.__fontSizeAdjust

    @fontSizeAdjust.setter
    @style_set_decorator
    def fontSizeAdjust(self, value=None, *args, **kwargs):
        self.__fontSizeAdjust = value

    @property
    @style_get_decorator
    def fontStretch(self):
        return self.__fontStretch

    @fontStretch.setter
    @style_set_decorator
    def fontStretch(self, value=None, *args, **kwargs):
        self.__fontStretch = value

    @property
    @style_get_decorator
    def hangingPunctuation(self):
        return self.__hangingPunctuation

    @hangingPunctuation.setter
    @style_set_decorator
    def hangingPunctuation(self, value=None, *args, **kwargs):
        self.__hangingPunctuation = value

    @property
    @style_get_decorator
    def height(self):
        return self.__height

    @height.setter
    @style_set_decorator
    def height(self, value=None, *args, **kwargs):
        self.__height = value

    @property
    @style_get_decorator
    def hyphens(self):
        return self.__hyphens

    @hyphens.setter
    @style_set_decorator
    def hyphens(self, value=None, *args, **kwargs):
        self.__hyphens = value

    @property
    @style_get_decorator
    def icon(self):
        return self.__icon

    @icon.setter
    @style_set_decorator
    def icon(self, value=None, *args, **kwargs):
        self.__icon = value

    @property
    @style_get_decorator
    def imageOrientation(self):
        return self.__imageOrientation

    @imageOrientation.setter
    @style_set_decorator
    def imageOrientation(self, value=None, *args, **kwargs):
        self.__imageOrientation = value

    @property
    @style_get_decorator
    def isolation(self):
        return self.__isolation

    @isolation.setter
    @style_set_decorator
    def isolation(self, value=None, *args, **kwargs):
        self.__isolation = value

    @property
    @style_get_decorator
    def justifyContent(self):
        return self.__justifyContent

    @justifyContent.setter
    @style_set_decorator
    def justifyContent(self, value=None, *args, **kwargs):
        self.__justifyContent = value

    @property
    @style_get_decorator
    def left(self):
        return self.__left

    @left.setter
    @style_set_decorator
    def left(self, value=None, *args, **kwargs):
        self.__left = value

    @property
    @style_get_decorator
    def letterSpacing(self):
        return self.__letterSpacing

    @letterSpacing.setter
    @style_set_decorator
    def letterSpacing(self, value=None, *args, **kwargs):
        self.__letterSpacing = value

    @property
    @style_get_decorator
    def lineHeight(self):
        return self.__lineHeight

    @lineHeight.setter
    @style_set_decorator
    def lineHeight(self, value=None, *args, **kwargs):
        self.__lineHeight = value

    @property
    @style_get_decorator
    def listStyle(self):
        return self.__listStyle

    @listStyle.setter
    @style_set_decorator
    def listStyle(self, value=None, *args, **kwargs):
        self.__listStyle = value

    @property
    @style_get_decorator
    def listStyleImage(self):
        return self.__listStyleImage

    @listStyleImage.setter
    @style_set_decorator
    def listStyleImage(self, value=None, *args, **kwargs):
        self.__listStyleImage = value

    @property
    @style_get_decorator
    def listStylePosition(self):
        return self.__listStylePosition

    @listStylePosition.setter
    @style_set_decorator
    def listStylePosition(self, value=None, *args, **kwargs):
        self.__listStylePosition = value

    @property
    @style_get_decorator
    def listStyleType(self):
        return self.__listStyleType

    @listStyleType.setter
    @style_set_decorator
    def listStyleType(self, value=None, *args, **kwargs):
        self.__listStyleType = value

    @property
    @style_get_decorator
    def margin(self):
        return self.__margin

    @margin.setter
    @style_set_decorator
    def margin(self, value=None, *args, **kwargs):
        self.__margin = value

    @property
    @style_get_decorator
    def marginBottom(self):
        return self.__marginBottom

    @marginBottom.setter
    @style_set_decorator
    def marginBottom(self, value=None, *args, **kwargs):
        self.__marginBottom = value

    @property
    @style_get_decorator
    def marginLeft(self):
        return self.__marginLeft

    @marginLeft.setter
    @style_set_decorator
    def marginLeft(self, value=None, *args, **kwargs):
        self.__marginLeft = value

    @property
    @style_get_decorator
    def marginRight(self):
        return self.__marginRight

    @marginRight.setter
    @style_set_decorator
    def marginRight(self, value=None, *args, **kwargs):
        self.__marginRight = value

    @property
    @style_get_decorator
    def marginTop(self):
        return self.__marginTop

    @marginTop.setter
    @style_set_decorator
    def marginTop(self, value=None, *args, **kwargs):
        self.__marginTop = value

    @property
    @style_get_decorator
    def maxHeight(self):
        return self.__maxHeight

    @maxHeight.setter
    @style_set_decorator
    def maxHeight(self, value=None, *args, **kwargs):
        self.__maxHeight = value

    @property
    @style_get_decorator
    def maxWidth(self):
        return self.__maxWidth

    @maxWidth.setter
    @style_set_decorator
    def maxWidth(self, value=None, *args, **kwargs):
        self.__maxWidth = value

    @property
    @style_get_decorator
    def minHeight(self):
        return self.__minHeight

    @minHeight.setter
    @style_set_decorator
    def minHeight(self, value=None, *args, **kwargs):
        self.__minHeight = value

    @property
    @style_get_decorator
    def minWidth(self):
        return self.__minWidth

    @minWidth.setter
    @style_set_decorator
    def minWidth(self, value=None, *args, **kwargs):
        self.__minWidth = value

    @property
    @style_get_decorator
    def navDown(self):
        return self.__navDown

    @navDown.setter
    @style_set_decorator
    def navDown(self, value=None, *args, **kwargs):
        self.__navDown = value

    @property
    @style_get_decorator
    def navIndex(self):
        return self.__navIndex

    @navIndex.setter
    @style_set_decorator
    def navIndex(self, value=None, *args, **kwargs):
        self.__navIndex = value

    @property
    @style_get_decorator
    def navLeft(self):
        return self.__navLeft

    @navLeft.setter
    @style_set_decorator
    def navLeft(self, value=None, *args, **kwargs):
        self.__navLeft = value

    @property
    @style_get_decorator
    def navRight(self):
        return self.__navRight

    @navRight.setter
    @style_set_decorator
    def navRight(self, value=None, *args, **kwargs):
        self.__navRight = value

    @property
    @style_get_decorator
    def navUp(self):
        return self.__navUp

    @navUp.setter
    @style_set_decorator
    def navUp(self, value=None, *args, **kwargs):
        self.__navUp = value

    @property
    @style_get_decorator
    def objectFit(self):
        return self.__objectFit

    @objectFit.setter
    @style_set_decorator
    def objectFit(self, value=None, *args, **kwargs):
        self.__objectFit = value

    @property
    @style_get_decorator
    def objectPosition(self):
        return self.__objectPosition

    @objectPosition.setter
    @style_set_decorator
    def objectPosition(self, value=None, *args, **kwargs):
        self.__objectPosition = value

    @property
    @style_get_decorator
    def opacity(self):
        return self.__opacity

    @opacity.setter
    @style_set_decorator
    def opacity(self, value=None, *args, **kwargs):
        self.__opacity = value

    @property
    @style_get_decorator
    def order(self):
        return self.__order

    @order.setter
    @style_set_decorator
    def order(self, value=None, *args, **kwargs):
        self.__order = value

    @property
    @style_get_decorator
    def orphans(self):
        return self.__orphans

    @orphans.setter
    @style_set_decorator
    def orphans(self, value=None, *args, **kwargs):
        self.__orphans = value

    @property
    @style_get_decorator
    def outline(self):
        return self.__outline

    @outline.setter
    @style_set_decorator
    def outline(self, value=None, *args, **kwargs):
        self.__outline = value

    @property
    @style_get_decorator
    def outlineColor(self):
        return self.__outlineColor

    @outlineColor.setter
    @style_set_decorator
    def outlineColor(self, value=None, *args, **kwargs):
        self.__outlineColor = value

    @property
    @style_get_decorator
    def outlineOffset(self):
        return self.__outlineOffset

    @outlineOffset.setter
    @style_set_decorator
    def outlineOffset(self, value=None, *args, **kwargs):
        self.__outlineOffset = value

    @property
    @style_get_decorator
    def outlineStyle(self):
        return self.__outlineStyle

    @outlineStyle.setter
    @style_set_decorator
    def outlineStyle(self, value=None, *args, **kwargs):
        self.__outlineStyle = value

    @property
    @style_get_decorator
    def outlineWidth(self):
        return self.__outlineWidth

    @outlineWidth.setter
    @style_set_decorator
    def outlineWidth(self, value=None, *args, **kwargs):
        self.__outlineWidth = value

    @property
    @style_get_decorator
    def overflow(self):
        return self.__overflow

    @overflow.setter
    @style_set_decorator
    def overflow(self, value=None, *args, **kwargs):
        self.__overflow = value

    @property
    @style_get_decorator
    def overflowX(self):
        return self.__overflowX

    @overflowX.setter
    @style_set_decorator
    def overflowX(self, value=None, *args, **kwargs):
        self.__overflowX = value

    @property
    @style_get_decorator
    def overflowY(self):
        return self.__overflowY

    @overflowY.setter
    @style_set_decorator
    def overflowY(self, value=None, *args, **kwargs):
        self.__overflowY = value

    @property
    @style_get_decorator
    def padding(self):
        return self.__padding

    @padding.setter
    @style_set_decorator
    def padding(self, value=None, *args, **kwargs):
        self.__padding = value

    @property
    @style_get_decorator
    def paddingBottom(self):
        return self.__paddingBottom

    @paddingBottom.setter
    @style_set_decorator
    def paddingBottom(self, value=None, *args, **kwargs):
        self.__paddingBottom = value

    @property
    @style_get_decorator
    def paddingLeft(self):
        return self.__paddingLeft

    @paddingLeft.setter
    @style_set_decorator
    def paddingLeft(self, value=None, *args, **kwargs):
        self.__paddingLeft = value

    @property
    @style_get_decorator
    def paddingRight(self):
        return self.__paddingRight

    @paddingRight.setter
    @style_set_decorator
    def paddingRight(self, value=None, *args, **kwargs):
        self.__paddingRight = value

    @property
    @style_get_decorator
    def paddingTop(self):
        return self.__paddingTop

    @paddingTop.setter
    @style_set_decorator
    def paddingTop(self, value=None, *args, **kwargs):
        self.__paddingTop = value

    @property
    @style_get_decorator
    def pageBreakAfter(self):
        return self.__pageBreakAfter

    @pageBreakAfter.setter
    @style_set_decorator
    def pageBreakAfter(self, value=None, *args, **kwargs):
        self.__pageBreakAfter = value

    @property
    @style_get_decorator
    def pageBreakBefore(self):
        return self.__pageBreakBefore

    @pageBreakBefore.setter
    @style_set_decorator
    def pageBreakBefore(self, value=None, *args, **kwargs):
        self.__pageBreakBefore = value

    @property
    @style_get_decorator
    def pageBreakInside(self):
        return self.__pageBreakInside

    @pageBreakInside.setter
    @style_set_decorator
    def pageBreakInside(self, value=None, *args, **kwargs):
        self.__pageBreakInside = value

    @property
    @style_get_decorator
    def perspective(self):
        return self.__perspective

    @perspective.setter
    @style_set_decorator
    def perspective(self, value=None, *args, **kwargs):
        self.__perspective = value

    @property
    @style_get_decorator
    def perspectiveOrigin(self):
        return self.__perspectiveOrigin

    @perspectiveOrigin.setter
    @style_set_decorator
    def perspectiveOrigin(self, value=None, *args, **kwargs):
        self.__perspectiveOrigin = value

    @property
    @style_get_decorator
    def position(self):
        return self.__position

    @position.setter
    @style_set_decorator
    def position(self, value=None, *args, **kwargs):
        self.__position = value

    @property
    @style_get_decorator
    def quotes(self):
        return self.__quotes

    @quotes.setter
    @style_set_decorator
    def quotes(self, value=None, *args, **kwargs):
        self.__quotes = value

    @property
    @style_get_decorator
    def resize(self):
        return self.__resize

    @resize.setter
    @style_set_decorator
    def resize(self, value=None, *args, **kwargs):
        self.__resize = value

    @property
    @style_get_decorator
    def right(self):
        return self.__right

    @right.setter
    @style_set_decorator
    def right(self, value=None, *args, **kwargs):
        self.__right = value

    @property
    @style_get_decorator
    def tableLayout(self):
        return self.__tableLayout

    @tableLayout.setter
    @style_set_decorator
    def tableLayout(self, value=None, *args, **kwargs):
        self.__tableLayout = value

    @property
    @style_get_decorator
    def tabSize(self):
        return self.__tabSize

    @tabSize.setter
    @style_set_decorator
    def tabSize(self, value=None, *args, **kwargs):
        self.__tabSize = value

    @property
    @style_get_decorator
    def textAlign(self):
        return self.__textAlign

    @textAlign.setter
    @style_set_decorator
    def textAlign(self, value=None, *args, **kwargs):
        self.__textAlign = value

    @property
    @style_get_decorator
    def textAlignLast(self):
        return self.__textAlignLast

    @textAlignLast.setter
    @style_set_decorator
    def textAlignLast(self, value=None, *args, **kwargs):
        self.__textAlignLast = value

    @property
    @style_get_decorator
    def textDecoration(self):
        return self.__textDecoration

    @textDecoration.setter
    @style_set_decorator
    def textDecoration(self, value=None, *args, **kwargs):
        self.__textDecoration = value

    @property
    @style_get_decorator
    def textDecorationColor(self):
        return self.__textDecorationColor

    @textDecorationColor.setter
    @style_set_decorator
    def textDecorationColor(self, value=None, *args, **kwargs):
        self.__textDecorationColor = value

    @property
    @style_get_decorator
    def textDecorationLine(self):
        return self.__textDecorationLine

    @textDecorationLine.setter
    @style_set_decorator
    def textDecorationLine(self, value=None, *args, **kwargs):
        self.__textDecorationLine = value

    @property
    @style_get_decorator
    def textDecorationStyle(self):
        return self.__textDecorationStyle

    @textDecorationStyle.setter
    @style_set_decorator
    def textDecorationStyle(self, value=None, *args, **kwargs):
        self.__textDecorationStyle = value

    @property
    @style_get_decorator
    def textIndent(self):
        return self.__textIndent

    @textIndent.setter
    @style_set_decorator
    def textIndent(self, value=None, *args, **kwargs):
        self.__textIndent = value

    @property
    @style_get_decorator
    def textJustify(self):
        return self.__textJustify

    @textJustify.setter
    @style_set_decorator
    def textJustify(self, value=None, *args, **kwargs):
        self.__textJustify = value

    @property
    @style_get_decorator
    def textOverflow(self):
        return self.__textOverflow

    @textOverflow.setter
    @style_set_decorator
    def textOverflow(self, value=None, *args, **kwargs):
        self.__textOverflow = value

    @property
    @style_get_decorator
    def textShadow(self):
        return self.__textShadow

    @textShadow.setter
    @style_set_decorator
    def textShadow(self, value=None, *args, **kwargs):
        self.__textShadow = value

    @property
    @style_get_decorator
    def textTransform(self):
        return self.__textTransform

    @textTransform.setter
    @style_set_decorator
    def textTransform(self, value=None, *args, **kwargs):
        self.__textTransform = value

    @property
    @style_get_decorator
    def top(self):
        return self.__top

    @top.setter
    @style_set_decorator
    def top(self, value=None, *args, **kwargs):
        self.__top = value

    @property
    @style_get_decorator
    def transform(self):
        return self.__transform

    @transform.setter
    @style_set_decorator
    def transform(self, value=None, *args, **kwargs):
        self.__transform = value

    @property
    @style_get_decorator
    def transformOrigin(self):
        return self.__transformOrigin

    @transformOrigin.setter
    @style_set_decorator
    def transformOrigin(self, value=None, *args, **kwargs):
        self.__transformOrigin = value

    @property
    @style_get_decorator
    def transformStyle(self):
        return self.__transformStyle

    @transformStyle.setter
    @style_set_decorator
    def transformStyle(self, value=None, *args, **kwargs):
        self.__transformStyle = value

    @property
    @style_get_decorator
    def transition(self):
        return self.__transition

    @transition.setter
    @style_set_decorator
    def transition(self, value=None, *args, **kwargs):
        self.__transition = value

    @property
    @style_get_decorator
    def transitionProperty(self):
        return self.__transitionProperty

    @transitionProperty.setter
    @style_set_decorator
    def transitionProperty(self, value=None, *args, **kwargs):
        self.__transitionProperty = value

    @property
    @style_get_decorator
    def transitionDuration(self):
        return self.__transitionDuration

    @transitionDuration.setter
    @style_set_decorator
    def transitionDuration(self, value=None, *args, **kwargs):
        self.__transitionDuration = value

    @property
    @style_get_decorator
    def transitionTimingFunction(self):
        return self.__transitionTimingFunction

    @transitionTimingFunction.setter
    @style_set_decorator
    def transitionTimingFunction(self, value=None, *args, **kwargs):
        self.__transitionTimingFunction = value

    @property
    @style_get_decorator
    def transitionDelay(self):
        return self.__transitionDelay

    @transitionDelay.setter
    @style_set_decorator
    def transitionDelay(self, value=None, *args, **kwargs):
        self.__transitionDelay = value

    @property
    @style_get_decorator
    def unicodeBidi(self):
        return self.__unicodeBidi

    @unicodeBidi.setter
    @style_set_decorator
    def unicodeBidi(self, value=None, *args, **kwargs):
        self.__unicodeBidi = value

    @property
    @style_get_decorator
    def userSelect(self):
        return self.__userSelect

    @userSelect.setter
    @style_set_decorator
    def userSelect(self, value=None, *args, **kwargs):
        self.__userSelect = value

    @property
    @style_get_decorator
    def verticalAlign(self):
        return self.__verticalAlign

    @verticalAlign.setter
    @style_set_decorator
    def verticalAlign(self, value=None, *args, **kwargs):
        self.__verticalAlign = value

    @property
    @style_get_decorator
    def visibility(self):
        return self.__visibility

    @visibility.setter
    @style_set_decorator
    def visibility(self, value=None, *args, **kwargs):
        self.__visibility = value

    @property
    @style_get_decorator
    def whiteSpace(self):
        return self.__whiteSpace

    @whiteSpace.setter
    @style_set_decorator
    def whiteSpace(self, value=None, *args, **kwargs):
        self.__whiteSpace = value

    @property
    @style_get_decorator
    def width(self):
        return self.__width

    @width.setter
    @style_set_decorator
    def width(self, value=None, *args, **kwargs):
        self.__width = value

    @property
    @style_get_decorator
    def wordBreak(self):
        return self.__wordBreak

    @wordBreak.setter
    @style_set_decorator
    def wordBreak(self, value=None, *args, **kwargs):
        self.__wordBreak = value

    @property
    @style_get_decorator
    def wordSpacing(self):
        return self.__wordSpacing

    @wordSpacing.setter
    @style_set_decorator
    def wordSpacing(self, value=None, *args, **kwargs):
        self.__wordSpacing = value

    @property
    @style_get_decorator
    def wordWrap(self):
        return self.__wordWrap

    @wordWrap.setter
    @style_set_decorator
    def wordWrap(self, value=None, *args, **kwargs):
        self.__wordWrap = value

    @property
    @style_get_decorator
    def widows(self):
        return self.__widows

    @widows.setter
    @style_set_decorator
    def widows(self, value=None, *args, **kwargs):
        self.__widows = value

    @property
    @style_get_decorator
    def zIndex(self):
        return self.__zIndex

    @zIndex.setter
    @style_set_decorator
    def zIndex(self, value=None, *args, **kwargs):
        self.__zIndex = value

    # @property
    # @style_get_decorator
    # def zoomAndPan(self):
    #     return self.__zoomAndPan

    # @zoomAndPan.setter
    # @style_set_decorator
    # def zoomAndPan(self, value=None, *args, **kwargs):
    #     self.__zoomAndPan = value

    # @property
    # @style_get_decorator
    # def zoomAndResize(self):
    #     return self.__zoomAndResize

    # @zoomAndResize.setter
    # @style_set_decorator
    # def zoomAndResize(self, value=None, *args, **kwargs):
    #     self.__zoomAndResize = value

    @property
    @style_get_decorator
    def zoom(self):
        return self.__zoom

    @zoom.setter
    @style_set_decorator
    def zoom(self, value=None, *args, **kwargs):
        self.__zoom = value

    # @property
    # @style_get_decorator
    # def zoomType(self):
    #     return self.__zoomType

    # @zoomType.setter
    # @style_set_decorator
    # def zoomType(self, value=None, *args, **kwargs):
    #     self.__zoomType = value

    # Modifies an existing CSS property or creates a new CSS property in the declaration block. """
    # def setProperty(self, property, value):
    # print('shut your fucking mouth!')
    # self[property] = value


class CSSStyleDeclaration(Style):
    """The CSSStyleDeclaration interface represents an object that is a CSS declaration block,
    and exposes style information and various style-related methods and properties.

    A CSSStyleDeclaration object can be exposed using three different APIs:

    Via HTMLElement.style, which deals with the inline styles of a single element (e.g., <div style="...">).
    Via the CSSStyleSheet API. For example, document.styleSheets[0].cssRules[0].style
    returns a CSSStyleDeclaration object on the first CSS rule in the document's first stylesheet.
    Via Window.getComputedStyle(), which exposes the CSSStyleDeclaration object as a read-only interface.
    """

    def __init__(self, parentNode=None, *args, **kwargs):
        # print("*** MADE A STYLE ***")
        # super(Style).__init__(*args, **kwargs)
        super().__init__(parentNode, *args, **kwargs)

    @property
    def cssText(self):
        """Textual representation of the declaration block, if and only if it is exposed via HTMLElement.style.
        Setting this attribute changes the inline style.
        If you want a text representation of a computed declaration block,
        you can get it with JSON.stringify()."""
        raise NotImplementedError

    @property
    def length(self):
        """The number of properties. See the item() method below."""
        raise NotImplementedError

    @property
    def parentRule(self):
        """The containing CSSRule."""
        raise NotImplementedError

    # @property
    # def cssFloat(self):
    #     """ Special alias for the float CSS property. """
    #     raise NotImplementedError

    def getPropertyPriority(self):
        """Returns the optional priority, "important"."""
        raise NotImplementedError

    def getPropertyValue(self):
        """Returns the property value given a property name."""
        raise NotImplementedError

    def item(self):
        """Returns a CSS property name by its index, or the empty string if the index is out-of-bounds.
        An alternative to accessing nodeList[i] (which instead returns undefined when i is out-of-bounds).
        This is mostly useful for non-JavaScript DOM implementations.
        """
        raise NotImplementedError

    def removeProperty(self):
        """Removes a property from the CSS declaration block."""
        raise NotImplementedError

    # Modifies an existing CSS property or creates a new CSS property in the declaration block. """
    def setProperty(self, property, value, priority=None):
        print("is this magic!")
        # self[property] = value
        setattr(self, property, value)

    def getPropertyCSSValue(self):
        """ Only supported via getComputedStyle in Firefox. Returns the property value as a
        CSSPrimitiveValue or null for shorthand properties."""
        raise NotImplementedError
